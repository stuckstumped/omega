"""
Burp Suite Connector Module
Handles all communication with Burp Suite REST API
Gracefully handles Community Edition limitations
"""
import requests
import json
import time
from typing import Optional, Dict, List, Any
from config import BURP_BASE_URL, BURP_API_KEY, TIMEOUT, RETRY_ATTEMPTS, COMMUNITY_EDITION
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Suppress SSL warnings for local Burp instances
urllib3.disable_warnings(InsecureRequestWarning)


class BurpConnector:
    """Manages connection and communication with Burp Suite"""

    def __init__(self, base_url: str = BURP_BASE_URL, api_key: str = BURP_API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.verify = False  # For local instances
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to Burp Suite API"""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", TIMEOUT)

        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                
                # Handle empty response
                if response.text:
                    return response.json() if response.headers.get('content-type') == 'application/json' else {"status": "success", "data": response.text}
                return {"status": "success"}
            except requests.exceptions.ConnectionError:
                if attempt < RETRY_ATTEMPTS - 1:
                    print(f"Connection failed. Retrying ({attempt + 1}/{RETRY_ATTEMPTS})...")
                    time.sleep(2)
                else:
                    return {"error": "Failed to connect to Burp Suite. Is it running?", "status": "error"}
            except requests.exceptions.RequestException as e:
                return {"error": str(e), "status": "error"}

        return {"error": "Max retries exceeded", "status": "error"}

    def check_status(self) -> Dict[str, Any]:
        """Check if Burp Suite is running and accessible"""
        return self._request("GET", "/")

    def get_version(self) -> Dict[str, Any]:
        """Get Burp Suite version information"""
        return self._request("GET", "/v1/burp/version")

    def get_site_map(self, url_filter: Optional[str] = None) -> Dict[str, Any]:
        """Get the current site map"""
        endpoint = "/v1/burp/sitemap"
        params = {}
        if url_filter:
            params["urlFilter"] = url_filter
        return self._request("GET", endpoint, params=params)

    def start_scan(self, url: str, scan_type: str = "all") -> Dict[str, Any]:
        """
        Start an active scan on a target URL
        scan_type: "all", "audit", "crawl"
        Note: Not available in Burp Community Edition
        """
        if COMMUNITY_EDITION:
            return {
                "error": "Active scanning is not available in Burp Suite Community Edition",
                "status": "error",
                "note": "Use Burp Professional or manually test with the AI-powered extension"
            }
        payload = {
            "urls": [url],
            "scanConfigurations": [scan_type],
        }
        return self._request("POST", "/v1/scans", json=payload)

    def start_spider(self, url: str) -> Dict[str, Any]:
        """
        Start web spidering on a target URL
        Note: Not available in Burp Community Edition
        """
        if COMMUNITY_EDITION:
            return {
                "error": "Web spidering is not available in Burp Suite Community Edition",
                "status": "error",
                "note": "Use Burp Professional or manually browse to discover URLs"
            }
        payload = {
            "urls": [url],
        }
        return self._request("POST", "/v1/spider", json=payload)

    def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """Get the status of an active scan"""
        return self._request("GET", f"/v1/scans/{scan_id}")

    def get_issues(self, url_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Get identified security issues
        Note: Limited availability in Burp Community Edition
        """
        if COMMUNITY_EDITION:
            return {
                "error": "Issue retrieval via API has limited support in Burp Suite Community Edition",
                "status": "error",
                "note": "Use the Burp UI Dashboard tab to view detected issues"
            }
        endpoint = "/v1/issues"
        params = {}
        if url_filter:
            params["urlFilter"] = url_filter
        return self._request("GET", endpoint, params=params)

    def get_proxy_history(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get recent proxy history entries
        Note: Limited availability in Burp Community Edition
        """
        if COMMUNITY_EDITION:
            return {
                "error": "Proxy history API has limited support in Burp Suite Community Edition",
                "status": "error",
                "note": "Use the Burp Proxy tab to browse history in the UI"
            }
        return self._request("GET", "/v1/http-history", params={"limit": limit})

    def send_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a custom request through Burp"""
        return self._request("POST", "/v1/http-request", json=request_data)

    def stop_scan(self, scan_id: str) -> Dict[str, Any]:
        """Stop an active scan"""
        return self._request("DELETE", f"/v1/scans/{scan_id}")

    def export_report(self, scan_id: str, report_type: str = "html") -> Dict[str, Any]:
        """Export scan results as a report"""
        payload = {"reportType": report_type}
        return self._request("GET", f"/v1/scans/{scan_id}/report", json=payload)


def create_connector() -> BurpConnector:
    """Factory function to create a BurpConnector instance"""
    return BurpConnector()

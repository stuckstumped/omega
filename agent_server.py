"""
Burp Suite Agent Server
Provides HTTP API for Burp extension communication
"""
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any
from agent import BurpSuiteAgent
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Burp extension communication"""

    # Class variable to store agent instance
    agent_instance = None

    def do_POST(self):
        """Handle POST requests from Burp extension"""
        try:
            # Parse request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            if not body:
                self.send_error(400, "Empty request body")
                return

            request_data = json.loads(body)
            action = request_data.get('action')

            logger.info(f"Received action: {action}")

            # Route to appropriate handler
            if action == 'analyze_traffic':
                response = self.handle_analyze_traffic(request_data)
            elif action == 'scan':
                response = self.handle_scan(request_data)
            elif action == 'spider':
                response = self.handle_spider(request_data)
            elif action == 'get_issues':
                response = self.handle_get_issues(request_data)
            elif action == 'status':
                response = self.handle_status(request_data)
            else:
                response = {"error": f"Unknown action: {action}", "status": "error"}

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request")
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            self.send_error(500, str(e))

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "service": "Burp Agent Server",
                "version": "1.0.0"
            }).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def handle_analyze_traffic(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze HTTP traffic"""
        try:
            request_text = request_data.get('request', '')
            response_text = request_data.get('response', '')

            # Simple analysis
            findings = []

            # Check for security headers in response
            if 'Content-Security-Policy' not in response_text:
                findings.append("Missing Content-Security-Policy header")
            if 'X-Frame-Options' not in response_text:
                findings.append("Missing X-Frame-Options header")
            if 'X-Content-Type-Options' not in response_text:
                findings.append("Missing X-Content-Type-Options header")

            # Check for sensitive data patterns
            if 'password' in request_text.lower():
                findings.append("Potential password data in request")
            if 'api_key' in request_text.lower() or 'apikey' in request_text.lower():
                findings.append("Potential API key in request")

            return {
                "status": "success",
                "findings": findings,
                "severity": "INFO" if len(findings) < 3 else "WARNING"
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def handle_scan(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate a scan"""
        try:
            url = request_data.get('url')
            scan_type = request_data.get('type', 'all')

            if not url:
                return {"status": "error", "error": "URL required"}

            if self.agent_instance and self.agent_instance.connected:
                result = self.agent_instance.connector.start_scan(url, scan_type)
                logger.info(f"Scan started for {url}")
                return {"status": "success", "scan_result": result}
            else:
                return {"status": "error", "error": "Agent not connected"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def handle_spider(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate web spidering"""
        try:
            url = request_data.get('url')

            if not url:
                return {"status": "error", "error": "URL required"}

            if self.agent_instance and self.agent_instance.connected:
                result = self.agent_instance.connector.start_spider(url)
                logger.info(f"Spider started for {url}")
                return {"status": "success", "spider_result": result}
            else:
                return {"status": "error", "error": "Agent not connected"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def handle_get_issues(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get identified security issues"""
        try:
            url_filter = request_data.get('url_filter')

            if self.agent_instance and self.agent_instance.connected:
                result = self.agent_instance.connector.get_issues(url_filter)
                logger.info("Issues retrieved")
                return {"status": "success", "issues": result}
            else:
                return {"status": "error", "error": "Agent not connected"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def handle_status(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get agent status"""
        try:
            if self.agent_instance:
                return {
                    "status": "success",
                    "agent_connected": self.agent_instance.connected,
                    "scans_active": len(self.agent_instance.scans)
                }
            else:
                return {"status": "error", "error": "Agent not initialized"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(format % args)


class BurpAgentServer:
    """HTTP server for Burp extension communication"""

    def __init__(self, host: str = 'localhost', port: int = 9999):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        self.agent = None

    def start(self, agent: BurpSuiteAgent):
        """Start the HTTP server"""
        self.agent = agent
        AgentRequestHandler.agent_instance = agent

        try:
            self.server = HTTPServer((self.host, self.port), AgentRequestHandler)
            logger.info(f"Starting Burp Agent Server on {self.host}:{self.port}")

            # Run server in background thread
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()

            logger.info(f"Burp Agent Server running on http://{self.host}:{self.port}")
            return True

        except Exception as e:
            logger.error(f"Failed to start server: {str(e)}")
            return False

    def stop(self):
        """Stop the HTTP server"""
        if self.server:
            logger.info("Stopping Burp Agent Server")
            self.server.shutdown()
            self.server.server_close()
            if self.thread:
                self.thread.join(timeout=5)
            logger.info("Burp Agent Server stopped")


def main():
    """Run agent with HTTP server"""
    import time

    # Create agent
    agent = BurpSuiteAgent()

    # Connect to Burp Suite
    if agent.connect():
        # Start HTTP server
        server = BurpAgentServer()
        if server.start(agent):
            logger.info("Server ready to receive requests from Burp extension")
            
            try:
                # Keep running
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                server.stop()
                agent.disconnect()
        else:
            logger.error("Failed to start server")
    else:
        logger.error("Failed to connect to Burp Suite")


if __name__ == "__main__":
    main()

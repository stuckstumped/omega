"""
Integration tests for Burp Agent Server
"""

import unittest
import json
import time
import threading
from http.client import HTTPConnection
from agent_server import BurpAgentServer
from agent import BurpSuiteAgent
from unittest.mock import Mock, patch, MagicMock


class TestBurpAgentServer(unittest.TestCase):
    """Test the Burp Agent Server"""

    def setUp(self):
        """Set up test fixtures"""
        self.server = BurpAgentServer(host='localhost', port=19999)
        self.agent = Mock(spec=BurpSuiteAgent)
        self.agent.connected = False
        self.agent.scans = {}

    def test_server_start_stop(self):
        """Test server start and stop"""
        self.agent.connected = True
        result = self.server.start(self.agent)
        self.assertTrue(result)
        
        # Give server time to start
        time.sleep(0.5)
        
        # Check health endpoint
        try:
            conn = HTTPConnection('localhost', 19999, timeout=5)
            conn.request('GET', '/health')
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data['status'], 'healthy')
            conn.close()
        finally:
            self.server.stop()

    def test_analyze_traffic_endpoint(self):
        """Test traffic analysis endpoint"""
        self.agent.connected = True
        self.server.start(self.agent)
        time.sleep(0.5)

        try:
            request_body = json.dumps({
                "action": "analyze_traffic",
                "request": "GET /api/users HTTP/1.1\r\nHost: example.com",
                "response": "HTTP/1.1 200 OK\r\nContent-Type: application/json"
            })

            conn = HTTPConnection('localhost', 19999, timeout=5)
            conn.request('POST', '/analyze', request_body)
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            
            data = json.loads(response.read().decode())
            self.assertEqual(data['status'], 'success')
            self.assertIn('findings', data)
            conn.close()
        finally:
            self.server.stop()

    def test_status_endpoint(self):
        """Test status endpoint"""
        self.agent.connected = True
        self.server.start(self.agent)
        time.sleep(0.5)

        try:
            request_body = json.dumps({"action": "status"})
            
            conn = HTTPConnection('localhost', 19999, timeout=5)
            conn.request('POST', '/status', request_body)
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            
            data = json.loads(response.read().decode())
            self.assertEqual(data['status'], 'success')
            self.assertTrue(data['agent_connected'])
            conn.close()
        finally:
            self.server.stop()

    def test_invalid_action(self):
        """Test invalid action handling"""
        self.agent.connected = True
        self.server.start(self.agent)
        time.sleep(0.5)

        try:
            request_body = json.dumps({"action": "invalid_action"})
            
            conn = HTTPConnection('localhost', 19999, timeout=5)
            conn.request('POST', '/', request_body)
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            
            data = json.loads(response.read().decode())
            self.assertEqual(data['status'], 'error')
            conn.close()
        finally:
            self.server.stop()


if __name__ == "__main__":
    unittest.main()

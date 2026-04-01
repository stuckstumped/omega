"""
Unit tests for Burp Suite Agent components
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from burp_connector import BurpConnector
from agent import BurpSuiteAgent


class TestBurpConnector(unittest.TestCase):
    """Test BurpConnector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.connector = BurpConnector()

    @patch('burp_connector.requests.Session.request')
    def test_check_status_success(self, mock_request):
        """Test successful status check"""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "running"}
        mock_response.text = '{"status": "running"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_request.return_value = mock_response

        result = self.connector.check_status()
        self.assertNotIn("error", result)

    @patch('burp_connector.requests.Session.request')
    def test_check_status_connection_error(self, mock_request):
        """Test connection error handling"""
        import requests
        mock_request.side_effect = requests.exceptions.ConnectionError()

        result = self.connector.check_status()
        self.assertIn("error", result)
        self.assertEqual(result["status"], "error")

    def test_connector_initialization(self):
        """Test connector initialization"""
        connector = BurpConnector("http://localhost:1337", "test-key")
        self.assertEqual(connector.base_url, "http://localhost:1337")


class TestBurpSuiteAgent(unittest.TestCase):
    """Test BurpSuiteAgent class"""

    def setUp(self):
        """Set up test fixtures"""
        self.agent = BurpSuiteAgent()

    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertFalse(self.agent.connected)
        self.assertIsNone(self.agent.connector)

    @patch('burp_connector.BurpConnector.check_status')
    def test_connect_success(self, mock_status):
        """Test successful connection"""
        mock_status.return_value = {}
        result = self.agent.connect()
        self.assertTrue(self.agent.connected)

    @patch('burp_connector.BurpConnector.check_status')
    def test_connect_failure(self, mock_status):
        """Test connection failure"""
        mock_status.return_value = {"error": "Connection failed"}
        result = self.agent.connect()
        self.assertFalse(self.agent.connected)

    def test_disconnect(self):
        """Test disconnection"""
        self.agent.connected = True
        self.agent.disconnect()
        self.assertFalse(self.agent.connected)

    @patch.object(BurpSuiteAgent, 'connector', create=True)
    def test_process_request_not_connected(self, mock_connector):
        """Test processing request when not connected"""
        self.agent.connected = False
        result = self.agent.process_request("status")
        self.assertEqual(result["status"], "error")

    def test_handle_help(self):
        """Test help command"""
        result = self.agent.handle_help("")
        self.assertEqual(result["status"], "success")

    def test_handle_unknown(self):
        """Test unknown command"""
        result = self.agent.handle_unknown("")
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()

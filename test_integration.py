"""
Standalone script to test Burp Extension integration
"""

import requests
import json
import time
from agent_server import BurpAgentServer
from agent import BurpSuiteAgent
import threading


def test_agent_server():
    """Test the agent server endpoints"""
    
    print("\n" + "="*60)
    print("Testing Burp Agent Server Integration")
    print("="*60 + "\n")

    # Start agent and server
    print("[1/5] Starting AI Agent...")
    agent = BurpSuiteAgent()
    
    print("[2/5] Connecting to Burp Suite...")
    # Note: This will fail if Burp is not running, which is OK for demo
    agent.connect()
    
    print("[3/5] Starting HTTP Server...")
    server = BurpAgentServer('localhost', 9999)
    server_started = server.start(agent)
    
    if not server_started:
        print("❌ Failed to start server")
        return False
    
    # Wait for server to start
    time.sleep(1)
    
    print("[4/5] Testing Endpoints...\n")
    
    # Test health endpoint
    try:
        print("  Testing /health endpoint...")
        response = requests.get('http://localhost:9999/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Health check: {data['status']}")
    except Exception as e:
        print(f"  ✗ Health check failed: {e}")
    
    # Test analyze_traffic endpoint
    try:
        print("\n  Testing traffic analysis...")
        payload = {
            "action": "analyze_traffic",
            "request": "GET /api/users HTTP/1.1\r\nHost: example.com\r\n\r\n",
            "response": "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        }
        response = requests.post('http://localhost:9999/analyze', 
                                json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Analyzed traffic")
            print(f"    Findings: {len(data.get('findings', []))} issues found")
            for finding in data.get('findings', [])[:3]:
                print(f"      - {finding}")
    except Exception as e:
        print(f"  ✗ Traffic analysis failed: {e}")
    
    # Test status endpoint
    try:
        print("\n  Testing status endpoint...")
        payload = {"action": "status"}
        response = requests.post('http://localhost:9999/status', 
                                json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Agent status retrieved")
            print(f"    Connected: {data.get('agent_connected', False)}")
            print(f"    Active scans: {data.get('scans_active', 0)}")
    except Exception as e:
        print(f"  ✗ Status check failed: {e}")
    
    print("\n[5/5] Cleanup...")
    server.stop()
    agent.disconnect()
    
    print("\n✅ Integration test completed\n")
    return True


def test_extension_communication():
    """Simulate extension communication"""
    
    print("\n" + "="*60)
    print("Simulating Burp Extension Communication")
    print("="*60 + "\n")

    # Start server
    agent = BurpSuiteAgent()
    agent.connect()
    
    server = BurpAgentServer('localhost', 9999)
    server.start(agent)
    time.sleep(1)

    print("[1/3] Simulating extension traffic capture...\n")
    
    # Simulate captured traffic
    captured_requests = [
        {
            "url": "https://example.com/api/users",
            "method": "GET",
            "request": "GET /api/users HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer token123",
            "response": "HTTP/1.1 200 OK\r\nContent-Type: application/json"
        },
        {
            "url": "https://example.com/login",
            "method": "POST",
            "request": "POST /login HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\npassword=secret123",
            "response": "HTTP/1.1 302 Found\r\nSet-Cookie: session=abc123"
        }
    ]

    print("[2/3] Analyzing captured traffic...\n")
    
    for req in captured_requests:
        payload = {
            "action": "analyze_traffic",
            "request": req["request"],
            "response": req["response"]
        }
        
        try:
            response = requests.post('http://localhost:9999/analyze',
                                    json=payload, timeout=5)
            data = response.json()
            
            print(f"URL: {req['url']}")
            print(f"Method: {req['method']}")
            print(f"Severity: {data.get('severity', 'UNKNOWN')}")
            print(f"Findings: {len(data.get('findings', []))}")
            for finding in data.get('findings', []):
                print(f"  ⚠️  {finding}")
            print()
        except Exception as e:
            print(f"Error analyzing: {e}\n")

    print("[3/3] Cleanup")
    server.stop()
    agent.disconnect()
    
    print("\n✅ Extension communication test completed\n")


def main():
    """Run all integration tests"""
    import sys
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║   Burp AI Agent - Integration Test Suite              ║")
    print("╚════════════════════════════════════════════════════════╝")

    try:
        # Test 1: Server startup and endpoints
        if not test_agent_server():
            sys.exit(1)

        # Test 2: Extension communication simulation
        test_extension_communication()
        
        print("╔════════════════════════════════════════════════════════╗")
        print("║   All Integration Tests Completed                     ║")
        print("╚════════════════════════════════════════════════════════╝\n")

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

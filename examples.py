"""
Example usage of the Burp Suite AI Agent
Shows how to use the agent programmatically
"""

from agent import BurpSuiteAgent


def example_basic_usage():
    """Example: Basic agent usage"""
    agent = BurpSuiteAgent()

    # Connect to Burp Suite
    if agent.connect():
        # Check status
        agent.process_request("status")

        # Get version
        agent.process_request("version")

        # Disconnect
        agent.disconnect()


def example_scan_workflow():
    """Example: Perform a security scan"""
    agent = BurpSuiteAgent()

    if agent.connect():
        # Start a scan
        print("\n=== Starting Security Scan ===")
        agent.process_request("scan https://example.com all")

        # Get site map to see discovered URLs
        print("\n=== Site Map ===")
        agent.process_request("sitemap")

        # Check for issues
        print("\n=== Security Issues ===")
        agent.process_request("issues")

        agent.disconnect()


def example_spider_workflow():
    """Example: Web spidering workflow"""
    agent = BurpSuiteAgent()

    if agent.connect():
        print("\n=== Starting Web Spider ===")
        agent.process_request("spider https://example.com")

        # Get proxy history to see captured requests
        print("\n=== Proxy History ===")
        agent.process_request("proxy 20")

        agent.disconnect()


def example_custom_request():
    """Example: Send a custom request"""
    agent = BurpSuiteAgent()

    if agent.connect():
        # Prepare custom request as JSON
        custom_request = """{
            "url": "https://example.com/api/users",
            "method": "GET",
            "headers": {
                "User-Agent": "Mozilla/5.0"
            }
        }"""

        print("\n=== Sending Custom Request ===")
        agent.process_request(f"request {custom_request}")

        agent.disconnect()


if __name__ == "__main__":
    print("Burp Suite Agent - Examples\n")
    print("Choose an example:")
    print("1. Basic Usage")
    print("2. Scan Workflow")
    print("3. Spider Workflow")
    print("4. Custom Request")
    print("5. Interactive Mode")

    choice = input("\nEnter choice (1-5): ").strip()

    if choice == "1":
        example_basic_usage()
    elif choice == "2":
        example_scan_workflow()
    elif choice == "3":
        example_spider_workflow()
    elif choice == "4":
        example_custom_request()
    elif choice == "5":
        agent = BurpSuiteAgent()
        agent.run_interactive()
    else:
        print("Invalid choice")

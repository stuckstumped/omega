"""
Burp Suite AI Agent
Main agent that processes user requests and interacts with Burp Suite
"""
import sys
from typing import Optional, Dict, Any
from burp_connector import create_connector, BurpConnector
from config import SUPPORTED_ACTIONS, VERBOSE_MODE, COMMUNITY_EDITION
from ai_service import get_ai_service
from system_prompt_manager import SystemPromptManager
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)


class BurpSuiteAgent:
    """AI Agent for interacting with Burp Suite"""

    def __init__(self):
        self.connector: Optional[BurpConnector] = None
        self.ai_service = get_ai_service()
        self.prompt_manager = SystemPromptManager()
        self.connected = False
        self.scans = {}

    def connect(self) -> bool:
        """Establish connection to Burp Suite"""
        try:
            self.connector = create_connector()
            response = self.connector.check_status()
            
            if "error" in response:
                print(f"{Fore.RED}✗ Connection failed: {response['error']}{Style.RESET_ALL}")
                return False
            
            self.connected = True
            edition = "Community" if COMMUNITY_EDITION else "Professional"
            print(f"{Fore.GREEN}✓ Connected to Burp Suite ({edition} Edition){Style.RESET_ALL}")
            
            if COMMUNITY_EDITION:
                print(f"{Fore.YELLOW}Note: Limited API features available. Focus on extension for AI analysis.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Type 'info' to see available commands.{Style.RESET_ALL}")
            
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Connection error: {str(e)}{Style.RESET_ALL}")
            return False

    def disconnect(self) -> bool:
        """Disconnect from Burp Suite"""
        self.connected = False
        self.connector = None
        print(f"{Fore.YELLOW}Disconnected from Burp Suite{Style.RESET_ALL}")
        return True

    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process user request and execute corresponding Burp action"""
        if not self.connected or not self.connector:
            return {"status": "error", "message": "Not connected to Burp Suite"}

        user_input = user_input.strip().lower()

        # Parse command and arguments
        parts = user_input.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        # Route to appropriate handler
        handlers = {
            "status": self.handle_status,
            "version": self.handle_version,
            "scan": self.handle_scan,
            "spider": self.handle_spider,
            "model": self.handle_model,
            "prompt": self.handle_prompt,
            "sitemap": self.handle_sitemap,
            "issues": self.handle_issues,
            "proxy": self.handle_proxy,
            "request": self.handle_request,
            "info": self.handle_info,
            "help": self.handle_help,
            "quit": self.handle_quit,
        }

        handler = handlers.get(command, self.handle_unknown)
        return handler(args)

    def handle_status(self, args: str) -> Dict[str, Any]:
        """Check Burp Suite status"""
        result = self.connector.check_status()
        if "error" not in result:
            print(f"{Fore.GREEN}✓ Burp Suite is running{Style.RESET_ALL}")
            return {"status": "success", "message": "Burp Suite is running"}
        else:
            print(f"{Fore.RED}✗ Error: {result['error']}{Style.RESET_ALL}")
            return result

    def handle_version(self, args: str) -> Dict[str, Any]:
        """Get Burp Suite version"""
        result = self.connector.get_version()
        if "error" not in result:
            print(f"{Fore.CYAN}Version: {result.get('version', 'Unknown')}{Style.RESET_ALL}")
            return {"status": "success", "version": result}
        else:
            print(f"{Fore.RED}✗ Error: {result['error']}{Style.RESET_ALL}")
            return result

    def handle_scan(self, args: str) -> Dict[str, Any]:
        """Start a scan on target URL"""
        if not args:
            print(f"{Fore.YELLOW}Usage: scan <url> [scan_type]{Style.RESET_ALL}")
            print(f"Scan types: all, audit, crawl")
            return {"status": "error", "message": "URL required"}

        parts = args.split(maxsplit=1)
        url = parts[0]
        scan_type = parts[1] if len(parts) > 1 else "all"

        print(f"{Fore.CYAN}Starting scan on {url}...{Style.RESET_ALL}")
        result = self.connector.start_scan(url, scan_type)

        if "error" not in result:
            scan_id = result.get("id", "unknown")
            self.scans[scan_id] = {"url": url, "type": scan_type, "status": "running"}
            print(f"{Fore.GREEN}✓ Scan started (ID: {scan_id}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {result['error']}{Style.RESET_ALL}")
            if "note" in result:
                print(f"{Fore.YELLOW}Note: {result['note']}{Style.RESET_ALL}")

        return result

    def handle_spider(self, args: str) -> Dict[str, Any]:
        """Start web spidering on target URL"""
        if not args:
            print(f"{Fore.YELLOW}Usage: spider <url>{Style.RESET_ALL}")
            return {"status": "error", "message": "URL required"}

        url = args.strip()
        print(f"{Fore.CYAN}Starting spider on {url}...{Style.RESET_ALL}")
        result = self.connector.start_spider(url)

        if "error" not in result:
            print(f"{Fore.GREEN}✓ Spider started{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {result['error']}{Style.RESET_ALL}")
            if "note" in result:
                print(f"{Fore.YELLOW}Note: {result['note']}{Style.RESET_ALL}")

        return result

    def handle_sitemap(self, args: str) -> Dict[str, Any]:
        """Get the site map"""
        print(f"{Fore.CYAN}Retrieving site map...{Style.RESET_ALL}")
        result = self.connector.get_site_map(args if args else None)

        if "error" not in result:
            items = result.get("items", [])
            print(f"{Fore.GREEN}✓ Found {len(items)} items in site map{Style.RESET_ALL}")
            for item in items[:10]:  # Show first 10
                print(f"  - {item.get('url', 'Unknown')}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more")
        else:
            print(f"{Fore.RED}✗ Error: {result['error']}{Style.RESET_ALL}")

        return result

    def handle_issues(self, args: str) -> Dict[str, Any]:
        """Get identified security issues"""
        print(f"{Fore.CYAN}Retrieving issues...{Style.RESET_ALL}")
        result = self.connector.get_issues(args if args else None)

        if "error" not in result:
            issues = result.get("issues", [])
            print(f"{Fore.GREEN}✓ Found {len(issues)} issues{Style.RESET_ALL}")
            for issue in issues[:5]:  # Show first 5
                print(f"  - {issue.get('name', 'Unknown')}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
        else:
            print(f"{Fore.RED}✗ {result['error']}{Style.RESET_ALL}")
            if "note" in result:
                print(f"{Fore.YELLOW}Note: {result['note']}{Style.RESET_ALL}")

        return result

    def handle_proxy(self, args: str) -> Dict[str, Any]:
        """Get proxy history"""
        limit = int(args) if args and args.isdigit() else 50
        print(f"{Fore.CYAN}Retrieving proxy history (limit: {limit})...{Style.RESET_ALL}")
        result = self.connector.get_proxy_history(limit)

        if "error" not in result:
            entries = result.get("entries", [])
            print(f"{Fore.GREEN}✓ Found {len(entries)} entries{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {result['error']}{Style.RESET_ALL}")
            if "note" in result:
                print(f"{Fore.YELLOW}Note: {result['note']}{Style.RESET_ALL}")

        return result

    def handle_request(self, args: str) -> Dict[str, Any]:
        """Send custom request (requires JSON data)"""
        if not args:
            print(f"{Fore.YELLOW}Usage: request <json_data>{Style.RESET_ALL}")
            return {"status": "error", "message": "JSON data required"}

        try:
            import json
            request_data = json.loads(args)
            result = self.connector.send_request(request_data)
            print(f"{Fore.GREEN}✓ Request sent{Style.RESET_ALL}")
            return result
        except json.JSONDecodeError:
            print(f"{Fore.RED}✗ Invalid JSON format{Style.RESET_ALL}")
            return {"status": "error", "message": "Invalid JSON"}

    def handle_info(self, args: str) -> Dict[str, Any]:
        """Display information about Burp edition and available features"""
        edition = "Community" if COMMUNITY_EDITION else "Professional"
        print(f"\n{Fore.CYAN}=== Burp Suite {edition} Edition ==={Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✓ Available Commands:{Style.RESET_ALL}")
        for cmd, description in SUPPORTED_ACTIONS.items():
            print(f"  {Fore.CYAN}{cmd:<15}{Style.RESET_ALL} - {description}")
        
        if COMMUNITY_EDITION:
            print(f"\n{Fore.YELLOW}⚠ Community Edition Limitations:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}× Active scanning is not available{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}× Web spidering is not available{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}× Limited API access to issues and proxy history{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}✓ What You CAN Do:{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Real-time AI traffic analysis with the Java extension{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Manual security testing with AI insights{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Custom system prompts and model selection{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Threat pattern detection (SQL injection, XSS, etc.){Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✓ Professional Edition Features:{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ All Community Edition features{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Automated active scanning{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Web spidering and crawling{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Full API access to all scanning features{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}=== Quick Tips ==={Style.RESET_ALL}")
        print(f"  1. Load the Java extension in Burp for real-time AI analysis")
        print(f"  2. Configure model: {Fore.YELLOW}model use ollama llama2{Style.RESET_ALL}")
        print(f"  3. Set system prompt: {Fore.YELLOW}prompt use owasp_expert{Style.RESET_ALL}")
        print(f"  4. Type {Fore.YELLOW}help{Style.RESET_ALL} for more commands\n")
        
        return {"status": "success", "message": "Info displayed"}

    def handle_help(self, args: str) -> Dict[str, Any]:
        """Display available commands"""
        
        print(f"\n{Fore.CYAN}=== Model Selection ==={Style.RESET_ALL}")
        print(f"  {Fore.GREEN}{'model list':<20}{Style.RESET_ALL} - List available models")
        print(f"  {Fore.GREEN}{'model status':<20}{Style.RESET_ALL} - Show current model")
        print(f"  {Fore.GREEN}{'model use <type> [model]':<20}{Style.RESET_ALL} - Switch AI model")
        print(f"  {Fore.YELLOW}Example: model use ollama llama2{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Example: model use huggingface{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}=== System Prompts ==={Style.RESET_ALL}")
        print(f"  {Fore.GREEN}{'prompt list':<20}{Style.RESET_ALL} - List available prompts")
        print(f"  {Fore.GREEN}{'prompt use <name>':<20}{Style.RESET_ALL} - Use a system prompt")
        print(f"  {Fore.GREEN}{'prompt show':<20}{Style.RESET_ALL} - Show current prompt")
        print(f"  {Fore.GREEN}{'prompt create <name>':<20}{Style.RESET_ALL} - Create custom prompt")
        print(f"  {Fore.YELLOW}Available: security_analyzer, owasp_expert, api_security, etc.{Style.RESET_ALL}\n")
        return {"status": "success", "message": "Help displayed"}

    def handle_model(self, args: str) -> Dict[str, Any]:
        """Handle model selection commands"""
        if not args:
            print(f"{Fore.YELLOW}Usage: model <list|status|use> [args]{Style.RESET_ALL}")
            return {"status": "error", "message": "Argument required"}

        parts = args.split(maxsplit=2)
        command = parts[0].lower()

        if command == "list":
            models = self.ai_service.list_available_models()
            print(f"{Fore.CYAN}Available AI Models:{Style.RESET_ALL}")
            for provider, model_list in models.items():
                print(f"\n  {Fore.GREEN}{provider.upper()}{Style.RESET_ALL}:")
                for model in model_list:
                    print(f"    - {model}")
            return {"status": "success", "models": models}

        elif command == "status":
            status = self.ai_service.get_status()
            print(f"{Fore.CYAN}AI Service Status:{Style.RESET_ALL}")
            print(f"  Provider: {Fore.GREEN}{status['provider_name']}{Style.RESET_ALL}")
            print(f"  System Prompt: {Fore.GREEN}{status['system_prompt']}{Style.RESET_ALL}")
            return {"status": "success", "ai_status": status}

        elif command == "use":
            if len(parts) < 2:
                print(f"{Fore.YELLOW}Usage: model use <provider> [model_name]{Style.RESET_ALL}")
                return {"status": "error", "message": "Provider required"}

            provider = parts[1].lower()
            model = parts[2] if len(parts) > 2 else None

            if self.ai_service.switch_provider(provider, model):
                return {"status": "success", "message": f"Switched to {provider}"}
            else:
                return {"status": "error", "message": f"Failed to switch to {provider}"}

        else:
            print(f"{Fore.RED}✗ Unknown model command: {command}{Style.RESET_ALL}")
            return {"status": "error", "message": f"Unknown command: {command}"}

    def handle_prompt(self, args: str) -> Dict[str, Any]:
        """Handle system prompt commands"""
        if not args:
            print(f"{Fore.YELLOW}Usage: prompt <list|use|show|create> [args]{Style.RESET_ALL}")
            return {"status": "error", "message": "Argument required"}

        parts = args.split(maxsplit=1)
        command = parts[0].lower()

        if command == "list":
            prompts = self.prompt_manager.list_prompts()
            print(f"{Fore.CYAN}Available System Prompts:{Style.RESET_ALL}")
            for prompt_name in prompts:
                description = self.prompt_manager.get_prompt_description(prompt_name)
                print(f"  {Fore.GREEN}{prompt_name:<25}{Style.RESET_ALL} - {description}")
            return {"status": "success", "prompts": prompts}

        elif command == "use":
            if len(parts) < 2:
                print(f"{Fore.YELLOW}Usage: prompt use <prompt_name>{Style.RESET_ALL}")
                return {"status": "error", "message": "Prompt name required"}

            prompt_name = parts[1].strip()
            if self.ai_service.set_system_prompt(prompt_name):
                return {"status": "success", "message": f"Using {prompt_name}"}
            else:
                return {"status": "error", "message": f"Prompt not found: {prompt_name}"}

        elif command == "show":
            current_prompt = self.ai_service.get_system_prompt()
            print(f"{Fore.CYAN}Current System Prompt:{Style.RESET_ALL}")
            print(current_prompt)
            return {"status": "success", "prompt": current_prompt}

        elif command == "create":
            if len(parts) < 2:
                print(f"{Fore.YELLOW}Usage: prompt create <name>{Style.RESET_ALL}")
                print(f"You will be prompted to enter the prompt content (type 'END' on a new line to finish)")
                return {"status": "error", "message": "Prompt name required"}

            prompt_name = parts[1].strip()
            print(f"{Fore.CYAN}Enter your custom system prompt (type 'END' on a new line to finish):{Style.RESET_ALL}")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                lines.append(line)

            prompt_content = "\n".join(lines)
            if self.prompt_manager.save_custom_prompt(prompt_name, prompt_content):
                print(f"{Fore.GREEN}✓ Custom prompt '{prompt_name}' created{Style.RESET_ALL}")
                return {"status": "success", "message": f"Created prompt: {prompt_name}"}
            else:
                return {"status": "error", "message": f"Failed to create prompt"}

        else:
            print(f"{Fore.RED}✗ Unknown prompt command: {command}{Style.RESET_ALL}")
            return {"status": "error", "message": f"Unknown command: {command}"}
        print(f"\n{Fore.CYAN}=== Burp Suite Agent - Available Commands ==={Style.RESET_ALL}")
        for action, description in SUPPORTED_ACTIONS.items():
            print(f"  {Fore.GREEN}{action:<10}{Style.RESET_ALL} - {description}")
        print(f"  {Fore.GREEN}{'help':<10}{Style.RESET_ALL} - Show this help message")
        print(f"  {Fore.GREEN}{'quit':<10}{Style.RESET_ALL} - Exit the agent\n")
        return {"status": "success", "message": "Help displayed"}

    def handle_quit(self, args: str) -> Dict[str, Any]:
        """Exit the agent"""
        print(f"{Fore.YELLOW}Exiting Burp Suite Agent...{Style.RESET_ALL}")
        sys.exit(0)

    def handle_unknown(self, args: str) -> Dict[str, Any]:
        """Handle unknown command"""
        print(f"{Fore.RED}✗ Unknown command. Type 'help' for available commands.{Style.RESET_ALL}")
        return {"status": "error", "message": "Unknown command"}

    def run_interactive(self):
        """Run the agent in interactive mode"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║   Burp Suite AI Agent                  ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")

        # Attempt connection
        if not self.connect():
            print(f"{Fore.YELLOW}Warning: Could not connect to Burp Suite{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Make sure Burp Suite is running and accessible at {self.connector.base_url if self.connector else 'localhost:1337'}{Style.RESET_ALL}\n")
            response = input(f"{Fore.CYAN}Continue anyway? (y/n): {Style.RESET_ALL}")
            if response.lower() != 'y':
                return

        print(f"{Fore.GREEN}✓ Ready for commands. Type 'help' for available commands.{Style.RESET_ALL}\n")

        while True:
            try:
                user_input = input(f"{Fore.CYAN}burp-agent> {Style.RESET_ALL}")
                if not user_input.strip():
                    continue
                self.process_request(user_input)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Burp Suite AI Agent")
    parser.add_argument("--command", help="Execute single command and exit")
    parser.add_argument("--host", default="localhost", help="Burp Suite host")
    parser.add_argument("--port", default="1337", help="Burp Suite port")

    args = parser.parse_args()

    agent = BurpSuiteAgent()

    if args.command:
        if agent.connect():
            agent.process_request(args.command)
    else:
        agent.run_interactive()


if __name__ == "__main__":
    main()

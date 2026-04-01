# Burp Suite AI Agent

A comprehensive AI-powered security testing platform that integrates with Burp Suite through both a Python agent interface and a native Java extension. Enables intelligent, autonomous security testing operations through conversational commands and real-time traffic analysis.

## 🎯 What You Get

This project combines:
- **Python AI Agent**: Interactive CLI for security testing operations
- **Java Burp Extension**: Real-time traffic interception and analysis
- **HTTP Bridge**: Seamless communication between components
- **REST API**: Programmatic access to all features

## Features

- **Easy Connection**: Connect to Burp Suite REST API with minimal configuration
- **Interactive Commands**: Execute security testing commands through natural language
- **Scan Management**: Start and monitor active scans
- **Web Spidering**: Perform automated web reconnaissance
- **Issue Tracking**: Retrieve identified security vulnerabilities
- **Proxy History**: Access captured HTTP requests/responses
- **Site Mapping**: View discovered URLs and structure
- **Custom Requests**: Send raw HTTP requests through Burp
- **Java Extension**: Real-time traffic analysis and interception
- **HTTP Bridge**: Native integration between Python and Burp Suite
- **Multiple AI Models**: Support for Ollama (local), HuggingFace (cloud), and local pattern matching
- **Custom System Prompts**: Define your own security analysis prompts
- **Flexible Model Selection**: Choose which AI provider and model to use

## Installation

### Prerequisites

- **Burp Suite Professional** 2021.9+ (full REST API support)
- **Python 3.7+**
- **Java 11+** (for extension building)
- **Maven 3.6+** (for building Java extension)

### Quick Start

1. **Clone or navigate to the repository**
   ```bash
   cd /workspaces/omega
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Burp Suite connection**
   ```bash
   cp .env.example .env
   # Edit .env with your Burp Suite connection details
   ```

4. **Option A: Run Python Agent Only**
   ```bash
   python agent.py
   ```

5. **Option B: Run with Java Extension (Full Integration)**
   
   a) Build the extension:
   ```bash
   mvn clean package
   ```
   
   b) Start the agent server:
   ```bash
   python agent_server.py
   ```
   
   c) Load the extension in Burp Suite:
   - Extensions → Add
   - Extension Type: Java
   - Select: `target/burp-ai-agent-extension-1.0.0.jar`

## Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      Burp Suite                              │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Burp AI Agent Extension (Java)                     │   │
│  │  ├── HTTP Handler (real-time traffic analysis)      │   │
│  │  ├── Communication Bridge (HTTP client)             │   │
│  │  └── Traffic Analyzer (security findings)           │   │
│  └─────────────────────────────────────────────────────┘   │
│              ↕ HTTP/JSON (port 9999)                        │
└──────────────────────────────────────────────────────────────┘
                         ↕ 
┌──────────────────────────────────────────────────────────────┐
│              Python AI Agent Server                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  agent_server.py (HTTP server)                       │   │
│  │  ├── Request routing                                │   │
│  │  ├── Traffic analysis                              │   │
│  │  └── JSON response building                        │   │
│  └──────────────────────────────────────────────────────┘   │
│              ↕ REST API (port 1337)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  agent.py (AI Logic)                                 │   │
│  │  ├── Command processing                             │   │
│  │  ├── User interaction                               │   │
│  │  └── Request routing                                │   │
│  └──────────────────────────────────────────────────────┘   │
│              ↕ REST API (port 1337)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  burp_connector.py (Burp REST API Client)            │   │
│  │  ├── Scanning                                        │   │
│  │  ├── Spidering                                       │   │
│  │  ├── Issue retrieval                                │   │
│  │  └── Proxy history                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Real-time Traffic Analysis** (when extension is loaded):
   - Burp intercepts HTTP traffic
   - Java extension captures request/response
   - Agent server analyzes for security issues
   - Results logged to Burp output

2. **User-Initiated Scans** (via Python agent):
   - User enters command: `scan https://target.com`
   - Python agent processes request
   - Burp REST API initiates scan
   - Results returned to user

3. **Extension Communication** (via HTTP bridge):
   - Extension sends JSON to agent server (port 9999)
   - Agent server routes request to appropriate handler
   - Handler processes request (scan, spider, analyze, etc.)
   - Response returned as JSON

### Setting up Burp Suite API

**For Burp Suite Professional:**
1. Open Burp Suite Preferences
2. Navigate to: Tools → Burp REST API
3. Enable "Enable Burp REST API"
4. Configure listening port (default: 1337)
5. Note any API key if authentication is enabled

**Default Configuration:**
```env
BURP_HOST=localhost
BURP_PORT=1337
AGENT_HOST=localhost
AGENT_PORT=9999
```

## Usage

### Python Agent - Interactive Mode

Run the agent in interactive mode:
```bash
python agent.py
```

Then use commands:
```
burp-agent> help                 # Show available commands
burp-agent> status               # Check Burp Suite status
burp-agent> version              # Get Burp version
burp-agent> scan https://target.com   # Start scan
burp-agent> spider https://target.com # Start spidering
burp-agent> sitemap              # View site map
burp-agent> issues               # List security issues
burp-agent> proxy 50             # Get last 50 proxy entries
burp-agent> quit                 # Exit agent
```

### Python Agent - Command-Line Mode

Execute a single command:
```bash
python agent.py --command "scan https://target.com"
```

### Agent Server Mode (for Java Extension)

Run the agent with HTTP server for extension communication:
```bash
python agent_server.py
```

This starts:
- Python agent (background, connected to Burp Suite)
- HTTP server (localhost:9999)
- Listening for requests from Burp extension

### Java Extension Integration

Once the server is running and extension is loaded:

1. **Real-time Traffic Analysis**
   - All HTTP traffic is automatically analyzed
   - Security findings appear in Burp output tab
   - No additional configuration needed

2. **Extension Endpoints**
   - `POST /analyze` - Analyze traffic
   - `POST /scan` - Initiate scan
   - `POST /spider` - Initiate spider
   - `GET /health` - Check server status

3. **Example Extension Request**
   ```bash
   curl -X POST http://localhost:9999/analyze \
     -H "Content-Type: application/json" \
     -d '{
       "action": "analyze_traffic",
       "request": "GET /api/users HTTP/1.1",
       "response": "HTTP/1.1 200 OK"
     }'
   ```

## Available Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `status` | `status` | Check if Burp Suite is running |
| `version` | `version` | Get Burp Suite version info |
| `scan` | `scan <url> [scan_type]` | Start active scan (all/audit/crawl) |
| `spider` | `spider <url>` | Start web spidering |
| `sitemap` | `sitemap [url_filter]` | Show site map |
| `issues` | `issues [url_filter]` | List security issues |
| `proxy` | `proxy [limit]` | Get proxy history (default 50) |
| `request` | `request <json>` | Send custom request via Burp |
| `model` | `model <list\|status\|use>` | Manage AI model provider |
| `prompt` | `prompt <list\|use\|create\|show>` | Manage system prompts |
| `help` | `help` | Show command help |
| `quit` | `quit` | Exit agent |

## Configuration

Edit `.env` to customize:

```env
# Burp Suite Connection
BURP_HOST=localhost                    # Burp Suite hostname
BURP_PORT=1337                         # Burp Suite API port
BURP_API_KEY=                          # API key if authentication is enabled
BURP_USE_HTTPS=False                   # Use HTTPS for connection

# Agent Server (for Extension)
AGENT_HOST=localhost                   # Agent server hostname
AGENT_PORT=9999                        # Agent server port

# Agent Settings
VERBOSE_MODE=True                      # Enable verbose output

# AI Model Provider (local, ollama, huggingface)
MODEL_PROVIDER=local

# Ollama Configuration
OLLAMA_MODEL=llama2
OLLAMA_HOST=localhost
OLLAMA_PORT=11434

# HuggingFace Configuration
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
HF_API_KEY=your_api_key_here

# System Prompt (security_analyzer, owasp_expert, api_security, etc.)
SYSTEM_PROMPT=security_analyzer
# Or set custom prompt directly
CUSTOM_SYSTEM_PROMPT=
```

### Extension Configuration

For the Java extension, also configure in `pom.xml`:

```xml
<properties>
    <burp.api.version>2021.9</burp.api.version>
    <agent.host>localhost</agent.host>
    <agent.port>9999</agent.port>
</properties>
```

## Architecture

```
omega/
├── agent.py              # Main agent with interactive interface
├── burp_connector.py     # Burp Suite API connector
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment configuration
└── README.md             # This file
```

## API Reference

### BurpConnector Methods

```python
from burp_connector import create_connector

connector = create_connector()

# Connection methods
connector.check_status()           # Verify Burp is running
connector.get_version()            # Get version info

# Scanning
connector.start_scan(url, scan_type)     # Start active scan
connector.start_spider(url)              # Start spider
connector.get_scan_status(scan_id)       # Check scan progress
connector.stop_scan(scan_id)             # Stop active scan

# Data retrieval
connector.get_site_map(url_filter)       # Get discovered URLs
connector.get_issues(url_filter)         # Get security issues
connector.get_proxy_history(limit)       # Get proxy history

# Advanced
connector.send_request(request_data)     # Send custom request
connector.export_report(scan_id, type)   # Export scan report
```

## Example Workflow

```bash
# 1. Start the agent
python agent.py

# 2. Check Burp is running
burp-agent> status

# 3. Start a scan
burp-agent> scan https://example.com

# 4. Check discovered URLs
burp-agent> sitemap

# 5. Review found issues
burp-agent> issues

# 6. Exit
burp-agent> quit
```

## Troubleshooting

### "Failed to connect to Burp Suite"
- Ensure Burp Suite is running
- Verify BURP_HOST and BURP_PORT in .env match your Burp configuration
- Check firewall rules allow connection to Burp API port

### "Connection refused"
- Burp Suite REST API may not be enabled
- Check Burp Preferences → Burp REST API
- Restart Burp Suite after enabling API

### SSL Certificate Errors
- Local Burp instances use self-signed certs
- Agent automatically disables SSL verification for localhost
- For remote instances, update code if needed

## Security Considerations

⚠️ **Important**: This agent should only be used for authorized security testing on systems you own or have explicit permission to test.

- Keep your Burp API key confidential
- Don't commit `.env` file with credentials to version control
- Use HTTPS when connecting to remote Burp instances
- Ensure Burp API is not exposed to untrusted networks

## License

Use responsibly for authorized security testing only.

## Support

For Burp Suite documentation:
- https://portswigger.net/burp/documentation

## Notes

- This agent is designed for Burp Suite Professional (full REST API support)
- Community Edition support is limited
- Requires Burp Suite 2021.9 or later for REST API
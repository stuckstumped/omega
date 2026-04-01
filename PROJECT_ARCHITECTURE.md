# Burp Suite AI Agent - Complete Project Guide

## Project Overview

The **Burp Suite AI Agent** is a cutting-edge security testing platform that combines:
- **Python AI Agent**: Intelligent security testing orchestration
- **Java Burp Extension**: Real-time traffic analysis with AI capabilities
- **HTTP Bridge**: Seamless communication between components
- **REST API**: Full programmatic access to all features

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                         Burp Suite UI                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              Burp AI Agent Extension (Java)                 │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  BurpAiAgentExtension                                  │ │ │
│  │  │  - Implements BurpExtension interface                 │ │ │
│  │  │  - Requests AI_FEATURES capability                    │ │ │
│  │  │  - Registers HTTP handler for traffic interception   │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                          ↕                                    │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  AiAgentHttpHandler                                    │ │ │
│  │  │  - Intercepts all HTTP traffic                        │ │ │
│  │  │  - Extracts request/response data                    │ │ │
│  │  │  - Routes to analysis                                │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                          ↕                                    │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  TrafficAnalyzer                                       │ │ │
│  │  │  - Prepares analysis payload                          │ │ │
│  │  │  - Calls AI features                                  │ │ │
│  │  │  - Formats results                                    │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                          ↕                                    │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  AiFeatures (Interface)                               │ │ │
│  │  │  ├── analyzeTraffic()                                 │ │ │
│  │  │  ├── predictVulnerabilities()                        │ │ │
│  │  │  ├── rateRiskLevel()                                 │ │ │
│  │  │  └── generateRecommendations()                       │ │ │
│  │  │                                                        │ │ │
│  │  │  AiFeaturesImpl (Implementation)                      │ │ │
│  │  │  - Pattern-based analysis                            │ │ │
│  │  │  - Risk assessment                                   │ │ │
│  │  │  - Vulnerability prediction                          │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                          ↕                                    │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  AgentCommunicationBridge                             │ │ │
│  │  │  - HTTP client to Python agent                       │ │ │
│  │  │  - JSON serialization                                │ │ │
│  │  │  - Error handling                                    │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                          ↕ (HTTP/JSON on port 9999)               │
└────────────────────────────────────────────────────────────────────┘
                               ↕
┌────────────────────────────────────────────────────────────────────┐
│             Python AI Agent Server (agent_server.py)               │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  AgentRequestHandler                                         │ │
│  │  - HTTP request processing                                  │ │
│  │  - Route handler selection                                  │ │
│  │  - JSON response formatting                                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                          ↕                                         │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BurpSuiteAgent (agent.py)                                   │ │
│  │  - Interactive CLI interface                                │ │
│  │  - Command routing                                          │ │
│  │  - User session management                                  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                          ↕                                         │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BurpConnector (burp_connector.py)                           │ │
│  │  - REST API communication with Burp                         │ │
│  │  - Scan initiation                                          │ │
│  │  - Spider control                                           │ │
│  │  - Issue retrieval                                          │ │
│  │  - Proxy history access                                     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                          ↕ (REST API on port 1337)                │
└────────────────────────────────────────────────────────────────────┘
                               ↕
┌────────────────────────────────────────────────────────────────────┐
│                    Burp Suite REST API                             │
│                  (localhost:1337)                                  │
└────────────────────────────────────────────────────────────────────┘
```

## Component Tree

```
omega/
├── Core Python Agent
│   ├── agent.py                    # Main interactive agent
│   ├── agent_server.py             # HTTP server for extension
│   ├── burp_connector.py           # Burp REST API client
│   └── config.py                   # Configuration management
│
├── Java Burp Extension
│   └── src/main/java/com/burp/agent/extension/
│       ├── BurpAiAgentExtension.java           # Main extension
│       ├── AgentCommunicationBridge.java       # HTTP client
│       ├── TrafficAnalyzer.java                # Traffic analysis
│       ├── api/
│       │   └── EnhancedCapability.java         # Capability enum
│       └── features/
│           ├── AiFeatures.java                 # Feature interface
│           └── AiFeaturesImpl.java              # Feature implementation
│
├── Build Configuration
│   ├── pom.xml                     # Maven build configuration
│   ├── requirements.txt            # Python dependencies
│   └── setup.sh                    # Quick setup script
│
├── Testing
│   ├── test_agent.py               # Unit tests for agent
│   ├── test_agent_server.py        # Server tests
│   └── test_integration.py         # Integration tests
│
├── Examples
│   └── examples.py                 # Usage examples
│
├── Configuration
│   ├── .env.example                # Example environment config
│   └── config.py                   # Runtime configuration
│
└── Documentation
    ├── README.md                   # Main documentation
    ├── QUICKSTART.md               # Quick start guide
    ├── BURP_EXTENSION.md           # Extension guide
    ├── ENHANCED_CAPABILITIES.md    # AI features guide
    └── PROJECT_ARCHITECTURE.md     # This file
```

## Data Flow Examples

### Real-Time Traffic Analysis

```
User browses in Burp Suite
         ↓
Burp intercepts HTTP request/response
         ↓
Java Extension HttpHandler.handleHttpRequestResponse()
         ↓
TrafficAnalyzer.analyzeInteraction()
         ↓
AiFeaturesImpl.analyzeTraffic()
         ↓
Pattern-based analysis:
  - Missing headers detection
  - Credentials detection
  - Information disclosure detection
         ↓
Result: AnalysisResult object
         ↓
Risk rating calculation
         ↓
Recommendations generation
         ↓
Log to Burp output tab
```

### User-Initiated Scan

```
User enters command in agent
         ↓
agent.py: process_request()
         ↓
agent.py: handle_scan()
         ↓
BurpConnector.start_scan()
         ↓
HTTP POST to Burp REST API
  https://localhost:1337/v1/scans
         ↓
Burp Suite starts scan
         ↓
Response returned to user
         ↓
Display results in console
```

### Extension → Python Agent Communication

```
Java Extension detects issue
         ↓
AgentCommunicationBridge.analyzeWithAgent()
         ↓
JSON payload creation
         ↓
HTTP POST to localhost:9999
         ↓
Python agent_server receives request
         ↓
AgentRequestHandler.do_POST()
         ↓
Route request to handler:
  - analyze_traffic → handle_analyze_traffic()
  - scan → handle_scan()
  - spider → handle_spider()
  - get_issues → handle_get_issues()
         ↓
Handler processes request
         ↓
JSON response returned
         ↓
Java Extension processes result
         ↓
Log findings to Burp
```

## Technology Stack

### Programming Languages
- **Python 3.7+**: Core agent logic
- **Java 11+**: Burp extension
- **JSON**: Data interchange format

### Frameworks & Libraries

**Python**
- `requests`: HTTP communication
- `python-dotenv`: Configuration management
- `colorama`: Colored terminal output
- `http.server`: Built-in HTTP server

**Java**
- `Burp Suite Montoya API 2021.9+`: Extension framework
- `GSON`: JSON processing
- `Apache HttpClient 5`: HTTP communication
- `Maven`: Build tool

### APIs
- **Burp Suite REST API**: Scanning, spidering, issue retrieval
- **Custom HTTP Server**: Extension communication

## Communication Protocols

### HTTP Endpoints

**Python Agent Server** (port 9999)
```
POST /analyze              - Analyze traffic
POST /scan                 - Initiate scan
POST /spider               - Initiate spider
POST /get_issues           - Retrieve issues
POST /status               - Get agent status
GET  /health               - Health check
```

**Burp Suite REST API** (port 1337)
```
GET  /                     - Status check
GET  /v1/burp/version      - Version info
POST /v1/scans             - Start scan
POST /v1/spider            - Start spider
GET  /v1/issues            - Get issues
GET  /v1/burp/sitemap      - Get site map
GET  /v1/http-history      - Get proxy history
POST /v1/http-request      - Send custom request
```

## Data Structures

### Traffic Analysis Request
```json
{
  "action": "analyze_traffic",
  "request": "HTTP request text",
  "response": "HTTP response text"
}
```

### Traffic Analysis Response
```json
{
  "status": "success",
  "findings": ["Finding 1", "Finding 2"],
  "severity": "WARNING",
  "recommendations": "Remediation steps..."
}
```

### Scan Request
```json
{
  "action": "scan",
  "url": "https://target.com",
  "type": "all"
}
```

## Installation & Setup

### Quick Setup
```bash
cd /workspaces/omega
./setup.sh
```

### Manual Setup

**Python Agent**
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Burp Suite details
```

**Java Extension**
```bash
mvn clean package
# Load JAR in Burp: Extensions → Add → Java → Select target/burp-ai-agent-extension-1.0.0.jar
```

## Running the System

### Mode 1: Python Agent Only
```bash
python agent.py
# Interactive CLI for manual testing
```

### Mode 2: Agent Server (for Extension)
```bash
python agent_server.py
# Runs HTTP server on port 9999
# Load extension in Burp Suite for real-time analysis
```

### Mode 3: Examples
```bash
python examples.py
# Choose example workflow to run
```

## Testing

### Unit Tests
```bash
python -m pytest test_agent.py -v
python -m pytest test_agent_server.py -v
```

### Integration Tests
```bash
python test_integration.py
```

## Configuration

### Environment Variables
```env
BURP_HOST=localhost        # Burp Suite hostname
BURP_PORT=1337            # Burp Suite REST API port
BURP_API_KEY=             # Optional API key
BURP_USE_HTTPS=False      # Use HTTPS

AGENT_HOST=localhost      # Agent server hostname
AGENT_PORT=9999          # Agent server port

VERBOSE_MODE=True         # Enable verbose logging
```

## Security Considerations

⚠️ **Critical**

1. **Traffic Handling**
   - All traffic is captured locally
   - No external transmission by default
   - Sensitive data is flagged

2. **Authentication**
   - Implement API authentication for production
   - Use HTTPS for remote connections
   - Protect API keys in environment

3. **Network**
   - Restrict access to agent ports
   - Use firewall rules
   - Don't expose to untrusted networks

4. **Data Privacy**
   - SSL/TLS for encrypted traffic
   - No logs of sensitive data
   - Clean up old analysis reports

## Performance Characteristics

| Operation | Time | Memory |
|-----------|------|--------|
| Traffic Analysis | ~50ms | ~1KB per request |
| Scan Initiation | 2-5s | ~5MB |
| Spider Start | 1-3s | ~3MB |
| Issue Retrieval | 1-10s | Variable |
| Extension Load | ~2s | ~20MB |

## Troubleshooting

### Extension Not Found
- Rebuild with Maven: `mvn clean package`
- Check Java version: Need 11+
- Verify JAR file exists

### Connection Refused
- Ensure Burp Suite running
- Check ports are correct
- Verify firewall settings

### Slow Analysis
- Check CPU/memory usage
- Disable analysis for static assets
- Increase thread pool size

### Analysis Not Appearing
- Verify extension is enabled
- Check agent server is running
- Review Burp output logs

## Contributing

To add new features:

1. **Python Side**
   - Add method to `BurpSuiteAgent`
   - Implement in agent handler
   - Update tests

2. **Java Side**
   - Add to `AiFeatures` interface
   - Implement in `AiFeaturesImpl`
   - Update Burp communication

3. **Documentation**
   - Update README
   - Add examples
   - Document API changes

## Future Enhancements

- Machine learning model integration
- Custom pattern rules
- Statistical anomaly detection
- Collaborative scanning
- Advanced reporting
- Cloud integration
- Mobile app support

## References

- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
- [Montoya API Guide](https://portswigger.net/burp/extender)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Maven Documentation](https://maven.apache.org/)

## License

Use responsibly for authorized security testing only.

---

**Last Updated**: April 1, 2026
**Version**: 1.0.0

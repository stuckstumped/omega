# Burp Suite AI Agent - Java Extension

This directory contains the Java Burp Suite extension that integrates with the Python AI Agent.

## Overview

The `BurpAiAgentExtension` is a Burp Suite extension that:
- Intercepts HTTP traffic in real-time
- Sends traffic to the Python AI Agent for analysis
- Initiates scans and spidering operations
- Retrieves security findings and recommendations

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         Burp Suite (Professional/Community)         │
├─────────────────────────────────────────────────────┤
│  BurpAiAgentExtension                               │
│  ├── HTTP Handler (traffic interception)            │
│  ├── Communication Bridge (HTTP client)             │
│  └── Traffic Analyzer (data extraction)             │
├─────────────────────────────────────────────────────┤
│                    (HTTP/JSON)                       │
│           HTTP POST requests on :9999               │
│                    (HTTP/JSON)                       │
├─────────────────────────────────────────────────────┤
│              Python AI Agent Server                  │
│  ├── agent_server.py (HTTP server)                  │
│  ├── agent.py (AI logic)                            │
│  └── burp_connector.py (Burp REST API)              │
└─────────────────────────────────────────────────────┘
```

## Building the Extension

### Prerequisites

- Java 11 or later
- Maven 3.6 or later
- Burp Suite 2021.9 or later (Professional)

### Build Steps

1. Navigate to the project root:
   ```bash
   cd /workspaces/omega
   ```

2. Build with Maven:
   ```bash
   mvn clean package
   ```

3. The compiled extension JAR will be at:
   ```
   target/burp-ai-agent-extension-1.0.0.jar
   ```

## Installation in Burp Suite

### For Burp Suite Professional

1. **Load the Extension**
   - Open Burp Suite
   - Go to: Extensions → Installed → Add
   - Choose Extension Type: Java
   - Select: `target/burp-ai-agent-extension-1.0.0.jar`
   - Click: Next → Close

2. **Verify Installation**
   - Check the Extensions panel
   - You should see "Burp AI Agent" listed
   - Check the Output tab for initialization messages

### For Burp Suite Community Edition

Community Edition has limited extension support. For full functionality, use Professional Edition.

## Configuration

Edit `.env` in the project root to configure connection:

```env
# Python Agent Server
AGENT_HOST=localhost
AGENT_PORT=9999

# Burp Suite API
BURP_HOST=localhost
BURP_PORT=1337
BURP_API_KEY=
```

## Running the Integration

### Step 1: Start the Python Agent Server

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Configure .env with your Burp Suite connection details
cp .env.example .env
# Edit .env as needed

# Start the agent server
python agent_server.py
```

You should see:
```
Starting Burp Agent Server on localhost:9999
Burp Agent Server running on http://localhost:9999
```

### Step 2: Load Extension in Burp Suite

- Follow the "Installation in Burp Suite" steps above
- The extension will automatically connect to the Python agent

### Step 3: Use the Agent

Traffic captured in Burp Suite will automatically be analyzed by the AI Agent:
- Check the Burp Output tab for analysis results
- Use Burp's built-in scanning features which now integrate with the AI Agent

## Extension Features

### Automatic Traffic Analysis

When enabled, the extension automatically:
1. Intercepts HTTP requests and responses
2. Analyzes for security issues
3. Sends findings to the Burp output

### Scan Integration

Trigger scans through the Python agent:
```python
# Via Python agent_server.py endpoint
POST /analyze HTTP/1.1
Content-Type: application/json

{
  "action": "scan",
  "url": "https://target.com",
  "type": "all"
}
```

### Issue Detection

The extension identifies:
- Missing security headers
- Sensitive data exposure
- Suspicious patterns
- Configuration issues

## API Reference

### Extension Request Format

All requests are JSON POST to `http://localhost:9999`:

```json
{
  "action": "analyze_traffic|scan|spider|get_issues|status",
  "url": "https://example.com",  # For scan/spider
  "request": "HTTP request text",  # For traffic analysis
  "response": "HTTP response text"  # For traffic analysis
}
```

### Response Format

```json
{
  "status": "success|error",
  "findings": [...],
  "severity": "INFO|WARNING|CRITICAL",
  "error": "Error message if status is error"
}
```

## Troubleshooting

### Extension fails to load
- Verify Java 11+ is installed
- Check that the JAR file is valid: `jar tf target/burp-ai-agent-extension-1.0.0.jar`
- Review Burp error logs

### No connection to Python agent
- Ensure `python agent_server.py` is running
- Check that `AGENT_HOST` and `AGENT_PORT` in `.env` are correct
- Verify firewall allows connections to port 9999

### Traffic not being analyzed
- Check the Burp Extensions tab output
- Verify the extension is enabled
- Ensure Python agent is connected to Burp Suite

### High memory usage
- The extension analyzes all traffic by default
- Consider disabling if testing high-traffic applications
- Monitor via Java profiler

## Development

### Project Structure

```
src/main/java/com/burp/agent/extension/
├── BurpAiAgentExtension.java       # Main extension class
├── AgentCommunicationBridge.java   # HTTP communication
└── TrafficAnalyzer.java            # Traffic analysis logic
```

### Building for Development

```bash
# Clean build
mvn clean compile

# Run tests
mvn test

# Package with all dependencies
mvn package
```

### Debug Mode

Add debug logging by modifying `BurpAiAgentExtension.java`:

```java
api.logging().logToOutput("[DEBUG] Analyzing: " + url);
```

## Security Considerations

⚠️ **Important**

- This extension captures HTTP traffic - be aware of sensitive data
- Only use on authorized testing targets
- Do not expose the agent server to untrusted networks
- Implement authentication if running on shared systems
- Always enable HTTPS for remote connections

## Integration with CI/CD

Example GitHub Actions workflow:

```yaml
- name: Build Burp Extension
  run: |
    cd /workspaces/omega
    mvn clean package
    
- name: Upload Extension
  uses: actions/upload-artifact@v2
  with:
    name: burp-extension
    path: target/burp-ai-agent-extension-1.0.0.jar
```

## Support and Issues

For issues with:
- **Python Agent**: See README.md
- **Java Extension**: Check Maven build output
- **Integration**: Verify both components are running and can communicate

## References

- [Burp Suite Montoya API](https://portswigger.net/burp/documentation/desktop/extensions)
- [Burp Suite REST API](https://portswigger.net/burp/documentation/desktop/api)
- Maven Documentation: https://maven.apache.org/

## License

This extension uses the Burp Suite Java API which is governed by PortSwigger's license terms.
Only use for authorized security testing.

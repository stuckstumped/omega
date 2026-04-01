# Burp Suite AI Agent - Quick Reference

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Burp Connection
Edit `.env` and set your Burp Suite connection details:
```env
BURP_HOST=localhost
BURP_PORT=1337
BURP_API_KEY=  # If authentication is enabled
```

### 3. Ensure Burp Suite API is Enabled
- Open Burp Suite Preferences
- Go to: Tools → Burp REST API
- Enable the REST API (default port: 1337)

### 4. Start the Agent
```bash
python agent.py
```

## Quick Command Reference

```text
help           → Show all available commands
status         → Check if Burp Suite is running
version        → Get Burp version info

scan <url> [type]    → Start a scan (type: all/audit/crawl)
spider <url>         → Start web spidering
sitemap [filter]     → Show discovered URLs
issues [filter]      → List security vulnerabilities
proxy [limit]        → View proxy history (default: 50)

request <json>       → Send custom request
quit           → Exit the agent
```

## Common Workflows

### Scan a Website
```
burp-agent> scan https://target.com all
burp-agent> sitemap
burp-agent> issues
```

### Spider and Explore
```
burp-agent> spider https://target.com
burp-agent> sitemap
burp-agent> proxy 100
```

### Check Security Issues
```
burp-agent> issues
burp-agent> issues target.com    # Filter by domain
```

## Python API Usage

```python
from burp_connector import create_connector

# Create connector
connector = create_connector()

# Start a scan
result = connector.start_scan("https://example.com", "all")
scan_id = result.get("id")

# Get issues
issues = connector.get_issues()

# Get site map
sitemap = connector.get_site_map()

# Get proxy history
history = connector.get_proxy_history(limit=50)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Ensure Burp Suite is running and API is enabled |
| API not found | Update BURP_PORT in .env to match Burp settings |
| SSL errors | Agent auto-disables SSL for localhost |
| Scan doesn't start | Verify URL is valid and Burp has permission |

## Running Examples

Interactive example menu:
```bash
python examples.py
```

Run tests:
```bash
python -m pytest test_agent.py -v
```

## Architecture

- **agent.py** - Main interactive agent
- **burp_connector.py** - REST API communication
- **config.py** - Configuration management
- **examples.py** - Usage examples
- **test_agent.py** - Unit tests

## Important Notes

⚠️ **Security**: Only use on systems you own or have explicit permission to test.

✓ **Authorization**: Ensure all security testing is authorized.

✓ **API Version**: Requires Burp Suite 2021.9+ for REST API support.

✓ **Professional**: Full REST API available in Professional Edition.

# Burp Suite AI Agent - How It Works

## Overview

The Burp Suite AI Agent is a three-layer intelligent security testing system that combines:
- **Java Burp Extension** - Real-time traffic interception
- **Python AI Agent** - Intelligent threat analysis
- **REST API Integration** - Automated security testing

---

## Complete Architecture

### **Stage 1: Traffic Interception (Java Extension)**

When the extension loads in Burp Suite:

```
Burp Users Browses Target Site
  ↓
HTTP Request/Response passes through Proxy
  ↓
Java Extension intercepts (ProxyMessageHandler)
  ↓
Pattern Detection (SQL injection, XSS, path traversal, etc.)
  ↓
Quick Decision: Suspicious or Safe?
```

**PatternDetection includes:**
- SQL Injection: `UNION SELECT`, `'; DROP`, `DELETE FROM`
- XSS: `<script>`, event handlers (`onerror=`, `onclick=`), `javascript:`
- Path Traversal: `../../../`, `%2e%2e`
- System Commands: `cmd.exe`, `exec xp_`

### **Stage 2: AI Analysis Decision**

If patterns are ambiguous or suspicious, the extension sends data to Python AI agent:

```
Java Extension sends JSON payload:
{
  "url": "https://target.com/api/login",
  "method": "POST",
  "body": "username=admin&password=test123",
  "type": "request",
  "statusCode": 200
}
  ↓
Python Agent Server (port 9999) receives request
  ↓
Loads selected system prompt from /prompts/
  ↓
Queries AI Model (Ollama or HuggingFace)
  ↓
Model analyzes: "Is this a threat?"
  ↓
Returns decision: INTERCEPT | DROP | CONTINUE | DO_NOT_INTERCEPT
```

### **Stage 3: Action & Logging**

The response from AI is converted to a `MessageReceivedAction` enum:

| AI Response | Enum Value | Burp Behavior |
|-------------|------------|---------------|
| INTERCEPT | `INTERCEPT` | Show in UI for user review |
| DROP | `DROP` | Block and discard message |
| CONTINUE | `CONTINUE` | Follow interception rules |
| DO_NOT_INTERCEPT | `DO_NOT_INTERCEPT` | Auto-forward without review |

---

## Real Example: SQL Injection Detection

```
Step 1: User browses to:
https://target.com/search?q='; DROP TABLE users;--

Step 2: Burp intercepts the request
Extension sees: "'; DROP TABLE users;--"

Step 3: Pattern check detects:
✓ Contains "; DROP" → SUSPICIOUS

Step 4: Extension sends to AI Agent:
{
  "url": "https://target.com/search",
  "body": "'; DROP TABLE users;--",
  "type": "request"
}

Step 5: Python Agent with system prompt "owasp_expert.txt":
"Analyze for SQL injection vulnerable to OWASP Top 10"

Step 6: AI Model (e.g., Ollama llama2):
Responds: "CRITICAL: This is SQL injection. Decision: INTERCEPT"

Step 7: Java Extension gets "INTERCEPT" response:
- Returns: MessageReceivedAction.INTERCEPT
- Burp UI displays request for user review
- User can approve, modify, or block

Step 8: Logging:
[AI Agent] SQL injection detected in /search: '; DROP TABLE users;--
```

---

## Component Details

### **Java Extension Components**

1. **BurpAiAgentExtension** (Entry Point)
   - Implements `BurpExtension` interface
   - Requests `AI_FEATURES` capability
   - Registers request and response handlers
   - Initializes UnloadingHandler for cleanup

2. **ProxyMessageHandler** (Request Interceptor)
   - Implements `ProxyRequestHandler` interface
   - Method: `handleRequest(InterceptedHttpMessage)`
   - Analyzes incoming HTTP requests
   - Returns `MessageReceivedAction` enum

3. **ProxyResponseHandlerImpl** (Response Interceptor)
   - Implements `ProxyResponseHandler` interface
   - Method: `handleResponse(InterceptedHttpMessage)`
   - Analyzes incoming HTTP responses
   - Checks for error pages, stack traces, security issues

4. **TrafficAnalyzer** (Analysis Utility)
   - Static methods for decision-making
   - Pattern detection helpers
   - Enum conversion utilities

5. **AgentCommunicationBridge** (HTTP Client)
   - Sends analysis requests to Python agent
   - JSON serialization/deserialization
   - Error handling and retries
   - Configurable host/port (default: localhost:9999)

### **Python Components**

1. **agent_server.py** (HTTP Server)
   - Listens on port 9999
   - Receives JSON payloads from Java extension
   - Routes to appropriate handler
   - Returns text-based decisions

2. **agent.py** (Interactive CLI)
   - User-facing command interface
   - Commands: `scan`, `spider`, `issues`, `proxy`, `request`
   - Direct Burp REST API integration

3. **ai_service.py** (AI Model Interface)
   - Loads system prompt from `/prompts/`
   - Queries Ollama or HuggingFace
   - Parses AI responses for action keywords
   - Supports custom models and prompts

4. **burp_connector.py** (Burp REST API)
   - Communicates with Burp Suite REST API (port 1337)
   - Initiates scans, spiders, crawls
   - Retrieves issues and vulnerabilities
   - Accesses proxy history

5. **config.py** (Configuration)
   - Loads `.env` settings
   - Model backend selection
   - System prompt configuration

---

## System Prompts(/prompts/)

Each prompt file defines the AI's behavior:

- **owasp_expert.txt** → Detects OWASP Top 10 vulnerabilities
- **pentest_report.txt** → Pentest-focused analysis
- **api_security.txt** → API endpoint security checks
- **compliance_checker.txt** → Regulatory compliance verification
- **developer_focused.txt** → Development-safe analysis
- **security_analyzer.txt** → General security analysis

**Example Prompt:**
```
You are an expert security analyst specializing in OWASP Top 10 vulnerabilities.
Analyze the following HTTP request for security threats.
Return your decision as one of: INTERCEPT, DROP, CONTINUE, DO_NOT_INTERCEPT.
If you detect a threat, respond with: INTERCEPT [threat description]
If safe, respond with: CONTINUE
```

---

## AI Model Selection

### **Ollama (Local)**
- Runs on localhost:11434
- Models: `llama2`, `mistral`, `neural-chat`, etc.
- Pros: Fast, private, offline-capable
- Cons: Requires local GPU for speed
- Setup: Download from ollama.ai

### **HuggingFace (Cloud)**
- Requires API token
- Models: `mistralai/Mistral-7B`, `meta-llama/Llama-2-7b-chat`, etc.
- Pros: Powerful, always updated
- Cons: Internet required, potential latency, API costs
- Setup: Get token from huggingface.co

---

## Configuration (.env)

```env
# Burp Suite Connection
BURP_HOST=localhost
BURP_PORT=1337
BURP_API_KEY=  # Optional if auth enabled

# AI Model Selection
MODEL_BACKEND=ollama  # or "huggingface"
MODEL_NAME=llama2
OLLAMA_HOST=localhost:11434
HUGGINGFACE_MODEL_ID=mistralai/Mistral-7B
HUGGINGFACE_API_TOKEN=hf_xxx

# System Prompt
SYSTEM_PROMPT_FILE=prompts/owasp_expert.txt
```

---

## End-to-End Data Flow Example

### Scenario: Detecting XSS in a Comment Field

```
1. User posts comment:
   POST /post/123/comment
   {"text": "<img src=x onerror='alert(1)'>"}

2. Java Extension intercepts POST:
   - Extracts body: "<img src=x onerror='alert(1)'>"
   - Pattern check: "onerror=" found → SUSPICIOUS

3. Extension sends to Python Agent:
   POST http://localhost:9999/analyze
   {
     "url": "/post/123/comment",
     "method": "POST",
     "body": "{\"text\": \"<img src=x onerror='alert(1)'>\"}",
     "type": "request"
   }

4. Python agent loads prompt: "owasp_expert.txt"
   System message: "You are security expert. Detect OWASP threats..."

5. Python queries AI model with prompt + request data

6. AI Model responds:
   "This is XSS (Reflected, OWASP A03:2021). Decision: INTERCEPT"

7. Python agent extracts keyword: "INTERCEPT"

8. Python returns to Java:
   "This is XSS (Reflected, OWASP A03:2021). Decision: INTERCEPT"

9. Java Extension converts to enum:
   MessageReceivedAction.INTERCEPT

10. Burp displays in UI:
    [Intercepted Request]
    POST /post/123/comment
    [AI Agent] Detected: XSS (Reflected, OWASP A03:2021)

11. User can:
    - Forward (approve)
    - Block (drop)
    - Modify and resend
```

---

## Logging & Debugging

All decisions are logged to Burp's output console:

```
[AI Agent] Initializing Burp AI Agent v1.0.0
[AI Agent] Proxy handlers registered with AI analysis enabled
[AI Agent] Suspicious request pattern detected: /search?q='; DROP
[AI Agent] Request flagged for review: /api/login
[AI Agent] Response: SQL injection detected
[AI Agent] Dropping request: /admin/delete
```

---

## Performance Characteristics

- **Pattern Detection**: <1ms per request (local, instant)
- **AI Analysis**: 1-5 seconds (Ollama local) or 2-10 seconds (HuggingFace cloud)
- **Network Overhead**: Minimal (JSON payloads ~1-5KB)
- **Memory**: Extension ~50MB + Python agent ~200MB-1GB (depends on model)
- **GPU Acceleration**: Optional but recommended for Ollama

---

## Security & Privacy

- ✅ All traffic analyzed locally (optional)
- ✅ Custom system prompts define analysis behavior
- ✅ No data leaves your network (Ollama mode)
- ✅ Burp REST API authenticated (if enabled)
- ✅ Python agent validates all inputs
- ✅ Extension runs in Burp sandbox

---

## Quick Start

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure connection
cp .env.example .env
# Edit .env with Burp details

# 3. Start AI agent server
python agent_server.py

# 4. Build Java extension
mvn clean package

# 5. Load extension in Burp
# Extensions → Add → target/burp-ai-agent-extension-1.0.0.jar

# 6. Traffic is analyzed automatically!
```

All traffic through Burp Proxy is now intelligently analyzed with AI!

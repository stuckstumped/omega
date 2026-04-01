# Burp Suite Community Edition Setup Guide

## Key Differences: Community vs Professional

Your Burp Suite Community Edition has **limited REST API support**, but the **Java extension still works perfectly** for real-time traffic analysis with AI.

| Feature | Professional | Community |
|---------|--------------|-----------|
| REST API (Full) | ✅ | ❌ |
| Active Scans (API) | ✅ | ❌ |
| Web Spider (API) | ✅ | ❌ |
| Java Extensions | ✅ | ✅ **YES** |
| Proxy Interception | ✅ | ✅ **YES** |
| Traffic Analysis | ✅ | ✅ **YES** |
| Real-time AI Analysis | ✅ | ✅ **YES** |

---

## What Works with Community Edition

### ✅ WORKS - Java Extension (Main Feature)

The **Java Burp Extension** is the core component and works perfectly:

- Real-time HTTP/HTTPS request interception
- Pattern-based threat detection (SQL injection, XSS, etc.)
- AI-powered security analysis via Python agent
- Request/response modification
- Custom system prompts
- Model selection (Ollama/HuggingFace)

### ✅ WORKS - Python Agent Server

The Python agent can analyze traffic even without API:

- Receives interception data from Java extension
- Applies AI models for threat classification
- Returns intelligent decisions
- Supports custom prompts

### ❌ DOESN'T WORK - Automated Scanning Features

These require Professional Edition API:

- `scan <url>` command (Active Scanning)
- `spider <url>` command (Web Crawling)
- API-based issue retrieval
- Automated vulnerability assessment

---

## Installation for Community Edition

### Step 1: Clone and Configure

```bash
cd /workspaces/omega

# Copy environment template
cp .env.example .env

# Edit .env with your Burp details
```

### Step 2: Edit .env

```env
# Burp Suite Connection (Community Edition)
BURP_HOST=localhost
BURP_PORT=1337
BURP_API_KEY=
BURP_USE_HTTPS=False

# Most of the API features won't work, focus on extension

# AI Model Settings (Local recommended for Community)
MODEL_PROVIDER=local
# Alternative: ollama or huggingface

# System Prompt Choice
SYSTEM_PROMPT=security_analyzer
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Build Java Extension

```bash
mvn clean package
```

### Step 5: Load Extension in Burp Community Edition

1. Open **Burp Suite Community Edition**
2. Go to **Extensions** tab (or Tools → Extensions)
3. Click **Add**
4. Extension Type: **Java**
5. File: Select `target/burp-ai-agent-extension-1.0.0.jar`
6. Click **Next** → **Finish**

The extension appears in the Extensions list with status **Loaded**.

### Step 6: Start AI Agent Server (Optional)

```bash
python agent_server.py
```

This starts the HTTP server on port 9999 that receives traffic analysis requests from the Java extension.

---

## How It Works with Community Edition

### Real-Time Traffic Analysis Flow

```
1. You browse a website through Burp Proxy
2. Request/Response passes through Burp
3. Java Extension intercepts automatically
4. Extension analyzes with patterns (instant)
5. If suspicious, sends to Python AI Agent
6. AI Model (Ollama/HuggingFace) analyzes
7. Decision returned to extension
8. Burp takes action (INTERCEPT/DROP/CONTINUE)
```

### Example: SQL Injection Detection

```
Request: GET /search?q='; DROP TABLE users;--

[Extension] Pattern check: "; DROP" found → SUSPICIOUS
[Extension] Sends to AI Agent on port 9999
[Python Agent] Analyzes with system prompt
[AI Model] "This is SQL injection"
[Extension] Returns: INTERCEPT
[Burp UI] Shows request for manual review
```

---

## What You Can Still Do

✅ **Manual Security Testing**
- Intercept requests/responses
- Modify payloads
- Replay requests
- Observe AI analysis

✅ **Proxy History Review**
- Browse captured traffic manually
- Use browser in Burp UI
- Analyze patterns with AI

✅ **Repeater + AI Analysis**
- Send requests through Repeater
- Modify and resend manually
- Get AI-powered insights

✅ **Local Scanning**
- Use AI extension for pattern detection
- Manual vulnerability assessment
- Real-time threat intelligence

---

## Configuration Options

### Option A: Minimal Setup (Recommended for Community)

```env
BURP_HOST=localhost
BURP_PORT=1337
MODEL_PROVIDER=local
SYSTEM_PROMPT=security_analyzer
```

Fast, no dependencies, works immediately.

### Option B: With Ollama (Better Detection)

Requirements: Ollama running locally

```bash
# Install Ollama from ollama.ai
# Run: ollama run llama2
```

```env
BURP_HOST=localhost
BURP_PORT=1337
MODEL_PROVIDER=ollama
OLLAMA_MODEL=llama2
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
SYSTEM_PROMPT=owasp_expert
```

### Option C: With HuggingFace (Cloud-Based)

Requirements: HuggingFace API key

```env
BURP_HOST=localhost
BURP_PORT=1337
MODEL_PROVIDER=huggingface
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
HF_API_KEY=hf_your_api_key_here
SYSTEM_PROMPT=owasp_expert
```

---

## Troubleshooting Community Edition

### Issue: "Cannot load extension JAR"

**Solution:** Make sure you built it properly:
```bash
mvn clean package -DskipTests
```

Then try loading the JAR file directly.

### Issue: "Extension loads but doesn't intercept"

**Solution:** Check Burp Proxy settings:
1. Proxy → Intercept is **OFF** (or configure as needed)
2. Extension registered successfully (check Extensions tab)
3. Restart Burp after loading extension

### Issue: "AI Agent not responding"

**Solution:** Start the Python agent server:
```bash
python agent_server.py
```

Check it's listening on port 9999:
```bash
netstat -tuln | grep 9999
# or: lsof -i :9999
```

### Issue: "ollama model not found"

**Solution:** Pull the model first:
```bash
ollama pull llama2
ollama run llama2
```

Then set in .env:
```env
OLLAMA_MODEL=llama2
OLLAMA_HOST=localhost:11434
```

---

## System Prompts Available

Choose based on your testing focus:

- **security_analyzer** (default) - General security analysis
- **owasp_expert** - OWASP Top 10 focus
- **api_security** - API endpoint vulnerabilities
- **compliance_checker** - Regulatory compliance
- **developer_focused** - Safe development analysis
- **pentest_report** - Penetration test style

Set in .env:
```env
SYSTEM_PROMPT=owasp_expert
```

---

## Performance with Community Edition

- **Pattern Detection**: <1ms (instant)
- **AI Analysis (local)**: 1-5 seconds
- **AI Analysis (Ollama)**: 2-10 seconds
- **AI Analysis (HuggingFace)**: 3-15 seconds

No scanning queue like Professional, so performance is consistent.

---

## Limitations to Understand

❌ **Cannot do automated scans** via the agent
- Use Burp UI manual features instead
- Or upgrade to Professional for automation

❌ **No crawling/spidering API**
- Manually explore target site
- Burp will passively capture from browsing

❌ **Limited programmatic API access**
- Focus on extension and manual testing
- Python agent works, but limited API coverage

✅ **Extension works perfectly**
- This is your main tool
- Real-time AI analysis is powerful

---

## Quick Start Checklist

- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env` and edit
- [ ] Build extension: `mvn clean package`
- [ ] Load extension in Burp Community Edition
- [ ] (Optional) Start Python agent: `python agent_server.py`
- [ ] Browse through Burp Proxy
- [ ] Watch Console for AI analysis
- [ ] Modify and test payloads manually

---

## Next Steps

1. **Load the Extension** - Most important step
2. **Browse a test site** - See traffic being analyzed
3. **Review Console output** - Watch AI decisions
4. **Test with payloads** - Try SQL injection, XSS, etc.
5. **Modify payloads manually** - Use Repeater + AI insights

The Community Edition is fully capable for manual security testing with AI-powered insights!

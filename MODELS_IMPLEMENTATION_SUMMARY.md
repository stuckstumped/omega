# AI Models & Custom Prompts - Quick Implementation Summary

## What Was Added

### New Python Modules (3 files)

1. **model_providers.py** (350+ lines)
   - `OllamaProvider`: Local LLM models via Ollama
   - `HuggingFaceProvider`: Cloud-based models via HuggingFace API
   - `LocalPatternsProvider`: Fallback pattern matching (no setup needed)

2. **system_prompt_manager.py** (200+ lines)
   - 6 built-in security-focused system prompts
   - Save/load/manage custom prompts
   - Export/import prompt templates

3. **ai_service.py** (150+ lines)
   - Central service manager for AI providers
   - Model switching and selection
   - System prompt management

### New Documentation (1 file)

**AI_MODELS_AND_PROMPTS.md** - Comprehensive guide covering:
- Model installation and setup
- System prompt management
- Workflow examples
- Troubleshooting

### Updated Files (5 files)

1. **agent.py**
   - `handle_model()` - Model selection commands
   - `handle_prompt()` - System prompt management
   - Updated help text

2. **config.py**
   - Model provider environment variables
   - System prompt configuration

3. **agent_server.py**
   - Integration with AI service

4. **.env.example**
   - New AI model configuration options

5. **requirements.txt**
   - Added `ollama` package

## How to Use

### 1. Using Local Pattern Matching (Default - No Setup)

```bash
python agent.py
burp-agent> model status
burp-agent> scan https://target.com
```

No external dependencies needed. Works immediately.

### 2. Using Ollama (Local LLM Models)

**Installation:**
```bash
# Download and install from https://ollama.ai
# Then pull a model
ollama pull llama2

# Or use faster model
ollama pull mistral
```

**Configuration:**
```bash
# Edit .env
MODEL_PROVIDER=ollama
OLLAMA_MODEL=llama2
```

**Usage:**
```bash
python agent.py
burp-agent> model status
# Shows: Ollama (llama2)

burp-agent> scan https://target.com
# Uses Ollama llama2 for intelligent analysis
```

### 3. Using HuggingFace (Cloud Models)

**Setup:**
```bash
# 1. Create account at https://huggingface.co
# 2. Get API token from Settings → Access Tokens
# 3. Edit .env
MODEL_PROVIDER=huggingface
HF_API_KEY=hf_xxxxxxxxxxxxx
```

**Usage:**
```bash
python agent.py
burp-agent> model status
# Shows: HuggingFace (Mistral-7B...)

burp-agent> scan https://target.com
```

## AI Model Commands

### View Available Models
```bash
burp-agent> model list
```

### Check Current Model
```bash
burp-agent> model status
```

### Switch Models
```bash
# Switch to Ollama
burp-agent> model use ollama llama2
burp-agent> model use ollama mistral

# Switch to HuggingFace
burp-agent> model use huggingface mistralai/Mistral-7B-Instruct-v0.1

# Switch to local
burp-agent> model use local
```

## System Prompt Commands

### View Available Prompts
```bash
burp-agent> prompt list
```

Output:
```
Available System Prompts:
  security_analyzer         - General security analysis
  owasp_expert              - OWASP Top 10 focused
  api_security              - API-specific analysis
  compliance_checker        - Compliance and regulations
  developer_focused         - Developer-friendly guidance
  pentest_report            - Professional report format
```

### Show Current Prompt
```bash
burp-agent> prompt show
```

### Switch Prompt
```bash
burp-agent> prompt use owasp_expert
burp-agent> scan https://target.com
```

### Create Custom Prompt
```bash
burp-agent> prompt create my_custom_prompt
# Enter your custom system prompt (type END when done)
```

## Built-in System Prompts

| Prompt | Use Case | Best For |
|--------|----------|----------|
| `security_analyzer` | General security analysis | Most situations |
| `owasp_expert` | OWASP Top 10 assessment | Comprehensive audits |
| `api_security` | API endpoint analysis | API testing |
| `compliance_checker` | Compliance verification | Regulated environments |
| `developer_focused` | Developer guidance | Development teams |
| `pentest_report` | Professional reporting | Client reports |

## Popular Model Recommendations

### For Speed & Good Quality (Recommended for Most Cases)
```bash
MODEL_PROVIDER=ollama
OLLAMA_MODEL=mistral
```

### For Accuracy & Detail
```bash
MODEL_PROVIDER=ollama
OLLAMA_MODEL=llama2
```

### For Cloud-Based (Always Available)
```bash
MODEL_PROVIDER=huggingface
HF_API_KEY=your_key
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
```

### For No Setup Required
```bash
# Default - no configuration needed
MODEL_PROVIDER=local
```

## Example Workflows

### Workflow 1: Quick API Security Check (No Setup)
```bash
python agent.py
burp-agent> prompt use api_security
burp-agent> spider https://api.target.com
burp-agent> issues
```

### Workflow 2: Rich Analysis with Ollama
```bash
# First time: ollama pull llama2
# Edit .env: MODEL_PROVIDER=ollama

python agent.py
burp-agent> model status
burp-agent> prompt use owasp_expert
burp-agent> scan https://target.com
burp-agent> issues
```

### Workflow 3: Compliance Audit
```bash
# Edit .env: MODEL_PROVIDER=huggingface, HF_API_KEY=...

python agent.py
burp-agent> prompt use compliance_checker
burp-agent> scan https://target.com
burp-agent> issues
```

### Workflow 4: Team Security Training
```bash
python agent.py
burp-agent> prompt use developer_focused
burp-agent> model use local  # Fast response
burp-agent> spider https://dev-app.local
burp-agent> issues
# Share findings with team
```

## Environment Variable Reference

```env
# Model Provider Selection
MODEL_PROVIDER=local                    # local, ollama, or huggingface

# Ollama Configuration (for local LLM)
OLLAMA_MODEL=llama2                     # llama2, mistral, neural-chat
OLLAMA_HOST=localhost
OLLAMA_PORT=11434

# HuggingFace Configuration (for cloud models)
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
HF_API_KEY=hf_xxxxxxxxxxxxx

# System Prompt Selection
SYSTEM_PROMPT=security_analyzer         # or any custom prompt name
CUSTOM_SYSTEM_PROMPT=                   # Optional: override SYSTEM_PROMPT
```

## Troubleshooting

### Ollama Commands Not Working
```bash
# Check if Ollama is running
curl http://localhost:11434/api/status

# If not running:
ollama serve

# If model not found:
ollama pull llama2
```

### HuggingFace Not Available
```bash
# Check API key
echo $HF_API_KEY

# Verify key in .env
cat .env | grep HF_API_KEY

# Test connection
curl -H "Authorization: Bearer $HF_API_KEY" \
  "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
```

### Model Analysis Slow
- Use faster model: `ollama pull mistral`
- Or use local: `model use local`
- Or use HuggingFace: Pre-cached models are faster

### Prompt Not Found
```bash
# List all available
burp-agent> prompt list

# Use exact name from list
burp-agent> prompt use exact_name
```

## Advanced: Creating Custom Prompts

Example custom prompt for IoT security:

```bash
burp-agent> prompt create iot_security
```

Enter:
```
You are an IoT security specialist analyzing web APIs for IoT devices.
Focus on:
- IoT-specific vulnerabilities
- Device authentication issues  
- Resource constraints (no heavy crypto, etc.)
- Firmware update security
- MQTT/CoAP protocol issues
- Sensor data validation

Check for:
1. Weak device authentication
2. Unencrypted firmware updates
3. Hardcoded credentials
4. Lack of rate limiting
5. Missing input validation
6. Privilege escalation risks

END
```

Then use it:
```bash
burp-agent> prompt use iot_security
burp-agent> scan https://iot-device-api.target.com
```

## Performance Characteristics

| Provider | Speed | Setup | Accuracy | Cost |
|----------|-------|-------|----------|------|
| Local | Instant | None | Good | Free |
| Ollama | 1-5s | Download | Excellent | Free |
| HuggingFace | 1-3s | API Key | Excellent | Free/Paid |

## Next Steps

1. **Read Full Documentation**
   ```bash
   cat AI_MODELS_AND_PROMPTS.md
   ```

2. **Try Different Models**
   ```bash
   # Test each one with same target
   burp-agent> model use local
   burp-agent> model use ollama llama2
   burp-agent> model use huggingface mistralai/Mistral-7B-Instruct-v0.1
   ```

3. **Create Custom Prompts**
   ```bash
   burp-agent> prompt create my_custom
   # Enter your specialized analysis prompt
   ```

4. **Combine Prompts and Models**
   ```bash
   burp-agent> model use ollama mistral
   burp-agent> prompt use api_security
   burp-agent> scan https://your-api.com
   ```

## Summary

✓ **3 AI Model Providers**: Local (default), Ollama (local LLM), HuggingFace (cloud)
✓ **6 Built-in System Prompts**: Security analyzer, OWASP expert, API security, compliance checker, developer-focused, pentest report
✓ **Custom Prompts**: Create and manage your own prompts
✓ **Easy Switching**: Switch models and prompts on the fly
✓ **Full Documentation**: See AI_MODELS_AND_PROMPTS.md

Start using it:
```bash
python agent.py
burp-agent> model status
burp-agent> help
```

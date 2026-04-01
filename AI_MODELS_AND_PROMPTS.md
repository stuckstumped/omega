# AI Models and Custom Prompts Guide

This guide explains how to configure and use different AI models and custom system prompts with the Burp Suite AI Agent.

## Overview

The Burp Suite AI Agent supports multiple AI model providers:

- **Local Pattern Matching** (default) - No external dependencies, no API keys needed
- **Ollama** - Local LLM models, privacy-focused
- **HuggingFace** - Cloud-based models, powerful options

And includes multiple built-in system prompts for different security roles.

## Setting Up AI Models

### Local Pattern Matching (Default)

No setup required. Built-in pattern matching works out of the box.

```bash
# Already configured by default
python agent.py
burp-agent> model status
```

### Installing and Using Ollama

Ollama allows you to run large language models locally on your machine.

#### Installation

1. **Download Ollama**
   - Visit https://ollama.ai
   - Download for your OS (macOS, Windows, Linux)
   - Install and start the service

2. **Pull a Model**
   ```bash
   # Pull a model (first time only)
   ollama pull llama2          # ~4GB download
   # or
   ollama pull mistral         # Faster, good for security analysis
   ```

3. **Configure in Agent**
   ```bash
   # Edit .env
   MODEL_PROVIDER=ollama
   OLLAMA_MODEL=llama2
   OLLAMA_HOST=localhost
   OLLAMA_PORT=11434
   ```

#### Popular Models for Security Analysis

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama2 | 7B | Medium | Excellent | General security analysis |
| mistral | 7B | Fast | Excellent | Quick vulnerability detection |
| neural-chat | 7B | Fast | Good | Conversational security advice |
| starling-lm | 7B | Medium | Excellent | Technical analysis |
| openchat | 7B | Very Fast | Good | Real-time analysis |

#### Using Ollama in Agent

```bash
# Start agent
python agent.py

# In agent prompt
burp-agent> model status
burp-agent> model use ollama llama2
burp-agent> model status
burp-agent> scan https://target.com
```

### HuggingFace Cloud Models

HuggingFace provides access to cutting-edge models via API.

#### Setup

1. **Create HuggingFace Account**
   - Visit https://huggingface.co
   - Sign up (free)
   - Go to Settings → Access Tokens
   - Create new token with "read" access

2. **Configure in Agent**
   ```bash
   # Edit .env
   MODEL_PROVIDER=huggingface
   HF_API_KEY=your_token_here
   HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
   ```

#### Popular Models for Security

| Model | Provider | Best For |
|-------|----------|----------|
| Mistral-7B | mistralai | Excellent for security, fast |
| Llama 2 | meta-llama | General-purpose security analysis |
| Zephyr-7B | HuggingFaceH4 | Instruction-following, precise |
| Hermes-2 | NousResearch | Long context, detailed analysis |

#### Using HuggingFace in Agent

```bash
# Make sure HF_API_KEY is set
export HF_API_KEY="hf_xxxxxxxxxxxx"

# Start agent
python agent.py

# In agent prompt
burp-agent> model status
burp-agent> model use huggingface mistralai/Mistral-7B-Instruct-v0.1
burp-agent> model status
burp-agent> scan https://target.com
```

## Switching Between Models

### List Available Models

```bash
burp-agent> model list
```

Output:
```
Available AI Models:

  LOCAL:
    - pattern_matching

  OLLAMA:
    - llama2
    - mistral
    - neural-chat
    - starling-lm
    - openchat
    - dolphin-mixtral

  HUGGINGFACE:
    - mistralai/Mistral-7B-Instruct-v0.1
    - meta-llama/Llama-2-7b-chat-hf
    - HuggingFaceH4/zephyr-7b-beta
    - NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
```

### Check Current Model

```bash
burp-agent> model status
```

Output:
```
AI Service Status:
  Provider: Ollama (llama2)
  System Prompt: security_analyzer
```

### Switch to Different Model

```bash
# Switch to Ollama with a different model
burp-agent> model use ollama mistral

# Switch to HuggingFace
burp-agent> model use huggingface mistralai/Mistral-7B-Instruct-v0.1

# Switch back to local
burp-agent> model use local
```

## System Prompts

System prompts guide how the AI model analyzes security issues.

### Built-in System Prompts

The agent includes 6 built-in system prompts optimized for different roles:

1. **security_analyzer** (default)
   - General-purpose security analysis
   - Balanced approach to vulnerability detection
   
2. **owasp_expert**
   - Focuses on OWASP Top 10
   - Detailed vulnerability classification
   - Best for comprehensive assessments
   
3. **api_security**
   - Specialized for API security
   - Checks authentication, rate limiting, data validation
   - Best for API testing
   
4. **compliance_checker**
   - Checks compliance requirements
   - GDPR, PCI-DSS, HIPAA, SOC2, ISO 27001
   - Best for regulated environments
   
5. **developer_focused**
   - Security guidance for developers
   - Practical recommendations
   - Includes code examples
   - Best for development teams
   
6. **pentest_report**
   - Professional penetration test format
   - Business-focused language
   - Best for client reports

### Using System Prompts

#### List Available Prompts

```bash
burp-agent> prompt list
```

Output:
```
Available System Prompts:
  security_analyzer         - General security analysis and vulnerability detection
  owasp_expert              - OWASP Top 10 focused security assessment
  api_security              - API-specific security analysis and recommendations
  compliance_checker        - Compliance and regulatory requirement checks
  developer_focused         - Developer-friendly security guidance
  pentest_report            - Professional penetration test reporting format
```

#### Show Current Prompt

```bash
burp-agent> prompt show
```

#### Switch to Different Prompt

```bash
burp-agent> prompt use owasp_expert
burp-agent> scan https://target.com
```

### Creating Custom System Prompts

Create your own system prompts tailored to your needs:

```bash
burp-agent> prompt create my_custom_prompt
```

You'll be prompted to enter your custom prompt. Example:

```
You are a security expert specializing in Python web applications.
Focus on:
- OWASP Top 10 vulnerabilities specific to Django/Flask
- Common Python security pitfalls
- Secure coding practices for Python applications
- Dependencies and package vulnerabilities

When analyzing code or traffic:
1. Check for common Python security issues
2. Verify secure handling of user input
3. Review authentication/authorization implementation
4. Check for secure defaults and proper error handling
5. Assess logging and monitoring capabilities

Type END on a new line when done.
```

Then use it:

```bash
burp-agent> prompt use my_custom_prompt
burp-agent> scan https://python-app.target.com
```

## Environment Variable Configuration

### Model Provider Settings

```env
# AI Model Provider (local, ollama, huggingface)
MODEL_PROVIDER=local

# Ollama Configuration
OLLAMA_MODEL=llama2
OLLAMA_HOST=localhost
OLLAMA_PORT=11434

# HuggingFace Configuration
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
HF_API_KEY=your_api_key_here

# System Prompt
SYSTEM_PROMPT=security_analyzer
CUSTOM_SYSTEM_PROMPT=  # Optional: override SYSTEM_PROMPT
```

## Performance Considerations

### Local Pattern Matching
- **Speed**: Instant (~50ms)
- **Accuracy**: Moderate (pattern-based)
- **Resource**: Minimal
- **Cost**: Free

### Ollama (Local)
- **Speed**: Medium (depends on model, 1-5s)
- **Accuracy**: High (full LLM)
- **Resource**: 6-12GB RAM per model
- **Cost**: Free (compute cost locally)

### HuggingFace (Cloud)
- **Speed**: Fast (1-3s)
- **Accuracy**: Excellent (latest models)
- **Resource**: Runs on HuggingFace servers
- **Cost**: Free tier available, paid options

## Troubleshooting

### "Ollama not available"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/status

# If not running, start Ollama
ollama serve

# Pull a model if needed
ollama pull llama2
```

### "HuggingFace not available"

```bash
# Check API key
echo $HF_API_KEY

# Verify it's in .env
cat .env | grep HF_API_KEY

# Test API access
curl -H "Authorization: Bearer $HF_API_KEY" \
  https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1
```

### Model Analysis is Slow

1. **For Ollama**: Use faster models (mistral instead of llama2)
2. **For HuggingFace**: Some models are cached, first request is slower
3. **For Cloud**: Check network connectivity

### Custom Prompt Not Found

```bash
burp-agent> prompt list  # List all available prompts
burp-agent> prompt use exact_name  # Use exact name from list
```

## Workflow Examples

### Example 1: API Security Assessment

```bash
# Set up for API security analysis
burp-agent> model use ollama mistral
burp-agent> prompt use api_security
burp-agent> scan https://api.target.com

# Review findings
burp-agent> issues
burp-agent> issues api.target.com
```

### Example 2: Compliance Check

```bash
# Set up for compliance checking
burp-agent> model use huggingface mistralai/Mistral-7B-Instruct-v0.1
burp-agent> prompt use compliance_checker
burp-agent> scan https://target.com

# Scan for compliance issues
burp-agent> issues
```

### Example 3: Development Team Security Review

```bash
# Set up developer-focused prompt
burp-agent> model use local  # Fast, local
burp-agent> prompt use developer_focused
burp-agent> spider https://dev-app.local:3000

# Generate security recommendations for team
burp-agent> issues
```

## Advanced Usage

### Combining Custom Prompts and Models

```python
# In Python code
from ai_service import get_ai_service

ai = get_ai_service()

# Switch to specific model and prompt
ai.switch_provider("ollama", "mistral")
ai.set_system_prompt("api_security")

# Analyze traffic
result = ai.analyze_traffic(request_data, response_data)
```

### Exporting and Importing Prompts

```bash
# Export a prompt to a file
burp-agent> prompt export security_analyzer my_prompt_export.txt

# Import a prompt from a file
burp-agent> prompt import my_imported_prompt my_prompt_file.txt
```

## Recommendations by Use Case

| Use Case | Model Provider | System Prompt | Reason |
|----------|---|---|---|
| Quick scanning | Local | security_analyzer | Instant, no setup |
| API testing | Ollama (mistral) | api_security | Fast + specialized |
| Compliance audit | HuggingFace | compliance_checker | Accurate + detailed |
| Team guidance | Ollama (llama2) | developer_focused | Thoughtful + practical |
| Client report | HuggingFace | pentest_report | Professional output |
| Development | Local | developer_focused | Resource-efficient |

## Cost Estimation

### Ollama (Local)
- **Initial**: Download 4-7GB model (~30 min on good connection)
- **Recurring**: Free (runs locally)
- **Total**: One-time download, then free forever

### HuggingFace (Cloud)
- **Free tier**: ~30,000 requests/month
- **Paid**: $9+/month for more requests
- **Calculation**: Average security scan = 5-10 API calls

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review system prompt descriptions
3. Test with local provider first
4. Check model provider documentation:
   - Ollama: https://ollama.ai
   - HuggingFace: https://huggingface.co/docs

## Further Reading

- [Ollama Documentation](https://github.com/ollama/ollama)
- [HuggingFace Hub](https://huggingface.co)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [System Prompts Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

"""
Configuration settings for the Burp Suite AI Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Burp Suite Connection Settings
BURP_HOST = os.getenv("BURP_HOST", "localhost")
BURP_PORT = os.getenv("BURP_PORT", "1337")
BURP_API_KEY = os.getenv("BURP_API_KEY", "")
BURP_USE_HTTPS = os.getenv("BURP_USE_HTTPS", "False").lower() == "true"

# Construct base URL
BURP_BASE_URL = f"{'https' if BURP_USE_HTTPS else 'http'}://{BURP_HOST}:{BURP_PORT}"

# Agent Settings
TIMEOUT = 30
RETRY_ATTEMPTS = 3
VERBOSE_MODE = os.getenv("VERBOSE_MODE", "True").lower() == "true"

# Model Provider Settings
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "local").lower()  # local, ollama, huggingface
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))

HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY", "")

# System Prompt
SYSTEM_PROMPT_NAME = os.getenv("SYSTEM_PROMPT", "security_analyzer")
CUSTOM_SYSTEM_PROMPT = os.getenv("CUSTOM_SYSTEM_PROMPT", "")

# Supported Burp Suite Actions
SUPPORTED_ACTIONS = {
    "scan": "Start an active scan on a target",
    "spider": "Perform web spidering on a target",
    "proxy": "Access the proxy history",
    "sitemap": "Retrieve the site map",
    "issues": "Get identified security issues",
    "request": "Send a custom request through Burp",
    "status": "Check Burp Suite status",
    "version": "Get Burp Suite version info",
    "model": "Select AI model provider",
    "prompt": "Manage custom system prompts",
}

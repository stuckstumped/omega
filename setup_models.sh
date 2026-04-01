#!/usr/bin/env bash
# Enhanced Burp AI Agent - Model Provider Setup Guide

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Burp AI Agent - Model Provider Setup                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi
echo "✓ Python 3 found"

# Check for .env
if [ ! -f ".env" ]; then
    echo "⚠ .env not found, creating from example..."
    cp .env.example .env
fi

# Check what models are available
echo ""
echo "Available Model Providers:"
echo "────────────────────────────────────────────────────────────"

# Check for Ollama
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found"
    echo "  Run: ollama pull llama2 (or mistral, neural-chat, etc.)"
else
    echo "⚠ Ollama not found"
    echo "  Install from: https://ollama.ai"
fi
echo ""

# Check for HuggingFace API key
if [ -z "$HF_API_KEY" ]; then
    echo "⚠ HF_API_KEY not set"
    echo "  Get one: https://huggingface.co/settings/tokens"
else
    echo "✓ HF_API_KEY configured"
fi
echo ""

echo "Local pattern matching is always available (default)"
echo ""

echo "────────────────────────────────────────────────────────────"
echo "To configure Ollama:"
echo "  1. Install from https://ollama.ai"
echo "  2. ollama pull llama2"
echo "  3. In .env: MODEL_PROVIDER=ollama"
echo "  4. python agent.py"
echo ""

echo "To configure HuggingFace:"
echo "  1. Get API key: https://huggingface.co/settings/tokens"
echo "  2. In .env: MODEL_PROVIDER=huggingface"
echo "  3. In .env: HF_API_KEY=your_key"
echo "  4. python agent.py"
echo ""

echo "To use local pattern matching (no setup):"
echo "  1. python agent.py"
echo "  2. Works immediately"
echo ""

echo "For full documentation:"
echo "  See AI_MODELS_AND_PROMPTS.md"
echo ""

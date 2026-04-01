"""
AI Service Manager
Manages model selection and system prompt handling
"""
from typing import Optional, Dict
from model_providers import ModelProvider, OllamaProvider, HuggingFaceProvider, LocalPatternsProvider
from system_prompt_manager import SystemPromptManager
from config import MODEL_PROVIDER, OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_PORT, HUGGINGFACE_MODEL, HUGGINGFACE_API_KEY, SYSTEM_PROMPT_NAME, CUSTOM_SYSTEM_PROMPT
from colorama import Fore, Style


class AIServiceManager:
    """Manages AI model providers and system prompts"""

    def __init__(self):
        self.provider: Optional[ModelProvider] = None
        self.prompt_manager = SystemPromptManager()
        self.current_provider_name = "local"
        self.current_prompt_name = SYSTEM_PROMPT_NAME
        self._initialize_provider()

    def _initialize_provider(self):
        """Initialize the active model provider"""
        provider_type = MODEL_PROVIDER.lower()

        if provider_type == "ollama":
            self.provider = OllamaProvider(OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_PORT)
            self.current_provider_name = "ollama"
            if self.provider.check_availability():
                print(f"{Fore.GREEN}✓ Ollama provider initialized ({OLLAMA_MODEL}){Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ Ollama not available, falling back to local{Style.RESET_ALL}")
                self.provider = LocalPatternsProvider()
                self.current_provider_name = "local"

        elif provider_type == "huggingface":
            self.provider = HuggingFaceProvider(HUGGINGFACE_MODEL, HUGGINGFACE_API_KEY)
            self.current_provider_name = "huggingface"
            if self.provider.check_availability():
                print(f"{Fore.GREEN}✓ HuggingFace provider initialized{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ HuggingFace not available, falling back to local{Style.RESET_ALL}")
                self.provider = LocalPatternsProvider()
                self.current_provider_name = "local"

        else:  # Default to local
            self.provider = LocalPatternsProvider()
            self.current_provider_name = "local"
            print(f"{Fore.GREEN}✓ Local pattern provider initialized{Style.RESET_ALL}")

    def get_system_prompt(self) -> str:
        """Get the active system prompt"""
        if CUSTOM_SYSTEM_PROMPT:
            return CUSTOM_SYSTEM_PROMPT
        return self.prompt_manager.get_prompt(self.current_prompt_name)

    def set_system_prompt(self, prompt_name: str) -> bool:
        """Set the active system prompt"""
        if prompt_name in self.prompt_manager.list_prompts():
            self.current_prompt_name = prompt_name
            print(f"{Fore.GREEN}✓ System prompt changed to: {prompt_name}{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}✗ Prompt '{prompt_name}' not found{Style.RESET_ALL}")
        return False

    def list_available_models(self) -> Dict[str, list]:
        """List available models by provider"""
        return {
            "local": ["pattern_matching"],
            "ollama": [
                "llama2",
                "mistral",
                "neural-chat",
                "starling-lm",
                "openchat",
                "dolphin-mixtral"
            ],
            "huggingface": [
                "mistralai/Mistral-7B-Instruct-v0.1",
                "meta-llama/Llama-2-7b-chat-hf",
                "HuggingFaceH4/zephyr-7b-beta",
                "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
            ]
        }

    def switch_provider(self, provider_type: str, model: Optional[str] = None) -> bool:
        """Switch to a different model provider"""
        provider_type = provider_type.lower()

        try:
            if provider_type == "ollama":
                model_name = model or OLLAMA_MODEL
                self.provider = OllamaProvider(model_name, OLLAMA_HOST, OLLAMA_PORT)
                if self.provider.check_availability():
                    self.current_provider_name = "ollama"
                    print(f"{Fore.GREEN}✓ Switched to Ollama ({model_name}){Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}✗ Ollama not available{Style.RESET_ALL}")
                    return False

            elif provider_type == "huggingface":
                model_name = model or HUGGINGFACE_MODEL
                api_key = HUGGINGFACE_API_KEY
                if not api_key:
                    print(f"{Fore.RED}✗ HuggingFace API key not configured{Style.RESET_ALL}")
                    return False
                
                self.provider = HuggingFaceProvider(model_name, api_key)
                if self.provider.check_availability():
                    self.current_provider_name = "huggingface"
                    print(f"{Fore.GREEN}✓ Switched to HuggingFace ({model_name}){Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}✗ HuggingFace not available{Style.RESET_ALL}")
                    return False

            elif provider_type == "local":
                self.provider = LocalPatternsProvider()
                self.current_provider_name = "local"
                print(f"{Fore.GREEN}✓ Switched to local pattern matching{Style.RESET_ALL}")
                return True

            else:
                print(f"{Fore.RED}✗ Unknown provider: {provider_type}{Style.RESET_ALL}")
                return False

        except Exception as e:
            print(f"{Fore.RED}✗ Error switching provider: {e}{Style.RESET_ALL}")
            return False

    def analyze_traffic(self, request: str, response: str) -> str:
        """Analyze traffic using current provider"""
        prompt = self.get_system_prompt()
        return self.provider.analyze_traffic(request, response, prompt)

    def predict_vulnerabilities(self, request: str) -> list:
        """Predict vulnerabilities using current provider"""
        prompt = self.get_system_prompt()
        return self.provider.predict_vulnerabilities(request, prompt)

    def generate_recommendations(self, url: str, findings: list) -> str:
        """Generate recommendations using current provider"""
        prompt = self.get_system_prompt()
        return self.provider.generate_recommendations(url, findings, prompt)

    def get_status(self) -> Dict[str, str]:
        """Get current AI service status"""
        return {
            "provider": self.current_provider_name,
            "provider_name": self.provider.name if self.provider else "Unknown",
            "system_prompt": self.current_prompt_name,
            "available": True if self.provider else False
        }


# Global AI service instance
_ai_service: Optional[AIServiceManager] = None


def get_ai_service() -> AIServiceManager:
    """Get or create the global AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIServiceManager()
    return _ai_service


def init_ai_service():
    """Initialize the AI service"""
    global _ai_service
    _ai_service = AIServiceManager()
    return _ai_service

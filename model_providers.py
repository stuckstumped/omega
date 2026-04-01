"""
Model Provider Interface and Implementations
Supports Ollama, HuggingFace, and local models
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import os
import json

class ModelProvider(ABC):
    """Abstract base class for model providers"""

    @abstractmethod
    def check_availability(self) -> bool:
        """Check if model provider is available"""
        pass

    @abstractmethod
    def analyze_traffic(self, request: str, response: str, system_prompt: str) -> str:
        """Analyze traffic using the model"""
        pass

    @abstractmethod
    def predict_vulnerabilities(self, request: str, system_prompt: str) -> List[str]:
        """Predict vulnerabilities using the model"""
        pass

    @abstractmethod
    def generate_recommendations(self, url: str, findings: List[str], system_prompt: str) -> str:
        """Generate security recommendations"""
        pass


class OllamaProvider(ModelProvider):
    """Ollama local LLM provider"""

    def __init__(self, model: str = "llama2", host: str = "localhost", port: int = 11434):
        """
        Initialize Ollama provider
        
        Args:
            model: Model name (llama2, mistral, neural-chat, etc.)
            host: Ollama server host
            port: Ollama server port
        """
        self.model = model
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.name = f"Ollama ({model})"

    def check_availability(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/status", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def analyze_traffic(self, request: str, response: str, system_prompt: str) -> str:
        """Analyze traffic using Ollama"""
        try:
            import requests
            
            prompt = f"""{system_prompt}

Analyze the following HTTP traffic for security issues:

REQUEST:
{request}

RESPONSE:
{response}

Provide a security analysis including:
1. Security findings
2. Severity level
3. Recommendations"""

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No response from model")
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Error analyzing with Ollama: {str(e)}"

    def predict_vulnerabilities(self, request: str, system_prompt: str) -> List[str]:
        """Predict vulnerabilities using Ollama"""
        try:
            import requests
            
            prompt = f"""{system_prompt}

Analyze this HTTP request for potential vulnerabilities:

{request}

List potential security vulnerabilities as a JSON array of strings.
Only return the JSON array, no additional text."""

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.2
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "[]").strip()
                
                # Extract JSON from response
                try:
                    if "[" in response_text:
                        json_str = response_text[response_text.find("["):response_text.rfind("]")+1]
                        return json.loads(json_str)
                except:
                    pass
                
            return []

        except Exception as e:
            return [f"Error predicting with Ollama: {str(e)}"]

    def generate_recommendations(self, url: str, findings: List[str], system_prompt: str) -> str:
        """Generate recommendations using Ollama"""
        try:
            import requests
            
            prompt = f"""{system_prompt}

Based on these security findings for {url}:
{json.dumps(findings, indent=2)}

Generate specific security improvement recommendations."""

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No recommendations available")
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Error generating recommendations with Ollama: {str(e)}"


class HuggingFaceProvider(ModelProvider):
    """HuggingFace cloud models provider"""

    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.1", api_key: Optional[str] = None):
        """
        Initialize HuggingFace provider
        
        Args:
            model: Model identifier (e.g., mistralai/Mistral-7B-Instruct-v0.1)
            api_key: HuggingFace API key (can also be set via HF_API_KEY env var)
        """
        self.model = model
        self.api_key = api_key or os.getenv("HF_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.name = f"HuggingFace ({model.split('/')[-1]})"

    def check_availability(self) -> bool:
        """Check if HuggingFace API is accessible"""
        if not self.api_key:
            return False
        
        try:
            import requests
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                f"{self.base_url}/{self.model}",
                headers=headers,
                timeout=10
            )
            return response.status_code in [200, 503]  # 503 means model is loading
        except Exception:
            return False

    def analyze_traffic(self, request: str, response: str, system_prompt: str) -> str:
        """Analyze traffic using HuggingFace"""
        try:
            import requests
            
            prompt = f"""{system_prompt}

Analyze the following HTTP traffic for security issues:

REQUEST:
{request}

RESPONSE:
{response}

Provide a security analysis including:
1. Security findings
2. Severity level
3. Recommendations"""

            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.3
                }
            }

            response = requests.post(
                f"{self.base_url}/{self.model}",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("generated_text", "No response from model")
                return str(data)
            else:
                return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error analyzing with HuggingFace: {str(e)}"

    def predict_vulnerabilities(self, request: str, system_prompt: str) -> List[str]:
        """Predict vulnerabilities using HuggingFace"""
        try:
            import requests
            
            prompt = f"""{system_prompt}

Analyze this HTTP request for potential vulnerabilities:

{request}

List potential security vulnerabilities as a JSON array of strings.
Only return the JSON array, no additional text."""

            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.2
                }
            }

            response = requests.post(
                f"{self.base_url}/{self.model}",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    response_text = data[0].get("generated_text", "[]")
                    
                    try:
                        if "[" in response_text:
                            json_str = response_text[response_text.find("["):response_text.rfind("]")+1]
                            return json.loads(json_str)
                    except:
                        pass
            
            return []

        except Exception as e:
            return [f"Error predicting with HuggingFace: {str(e)}"]

    def generate_recommendations(self, url: str, findings: List[str], system_prompt: str) -> str:
        """Generate recommendations using HuggingFace"""
        try:
            import requests
            
            prompt = f"""{system_prompt}

Based on these security findings for {url}:
{json.dumps(findings, indent=2)}

Generate specific security improvement recommendations."""

            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.3
                }
            }

            response = requests.post(
                f"{self.base_url}/{self.model}",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("generated_text", "No recommendations available")
                return str(data)
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Error generating recommendations with HuggingFace: {str(e)}"


class LocalPatternsProvider(ModelProvider):
    """Fallback provider using local pattern matching (no LLM required)"""

    def __init__(self):
        self.name = "Local Pattern Matching"

    def check_availability(self) -> bool:
        """Always available"""
        return True

    def analyze_traffic(self, request: str, response: str, system_prompt: str) -> str:
        """Analyze using local patterns"""
        findings = []
        
        if not response.get("X-Frame-Options"):
            findings.append("Missing X-Frame-Options header")
        if not response.get("Content-Security-Policy"):
            findings.append("Missing Content-Security-Policy header")
        if "password=" in request.lower():
            findings.append("Potential password in request")
        if "api_key" in request.lower() or "apikey" in request.lower():
            findings.append("Potential API key in request")
        
        return f"""Analysis Results:
Severity: {'WARNING' if len(findings) > 0 else 'SAFE'}
Findings: {len(findings)}
Results: {', '.join(findings) if findings else 'No issues found'}"""

    def predict_vulnerabilities(self, request: str, system_prompt: str) -> List[str]:
        """Predict using local patterns"""
        predictions = []
        
        if "union select" in request.lower():
            predictions.append("Potential SQL Injection")
        if "javascript:" in request or "onerror=" in request:
            predictions.append("Potential XSS vulnerability")
        if ".." in request or "../" in request:
            predictions.append("Potential Path Traversal")
        
        return predictions

    def generate_recommendations(self, url: str, findings: List[str], system_prompt: str) -> str:
        """Generate using local patterns"""
        recommendations = []
        
        for finding in findings:
            if "X-Frame-Options" in finding:
                recommendations.append("Add X-Frame-Options header to prevent clickjacking")
            elif "CSP" in finding:
                recommendations.append("Implement Content-Security-Policy header")
            elif "password" in finding.lower():
                recommendations.append("Never transmit passwords in plain text")
        
        return "\n".join(recommendations) if recommendations else "Review security configurations"

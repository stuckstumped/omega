"""
Custom System Prompt Management
Allows users to define and use custom system prompts for AI analysis
"""
import os
import json
from typing import Dict, List, Optional
from pathlib import Path

class SystemPromptManager:
    """Manages custom system prompts for AI analysis"""

    PROMPTS_DIR = Path("./prompts")
    DEFAULT_PROMPTS = {
        "security_analyzer": """You are an expert security analyst specializing in web application security.
Your role is to identify security vulnerabilities, assess risks, and provide remediation recommendations.
Focus on: OWASP Top 10, common misconfigurations, authentication/authorization issues, data exposure.
Be precise and actionable in your recommendations.""",

        "owasp_expert": """You are an OWASP security expert analyzing web applications.
Check for: Injection attacks (SQL, NoSQL, LDAP), Broken Authentication, Sensitive Data Exposure,
XML External Entities, Broken Access Control, Security Misconfiguration, Cross-Site Scripting,
Insecure Deserialization, Using Components with Known Vulnerabilities, Insufficient Logging.
Provide severity ratings and concrete remediation steps.""",

        "api_security": """You are an API security specialist.
Analyze API endpoints for security issues including: authentication/authorization flaws,
data validation problems, rate limiting absence, injection vulnerabilities, insecure data exposure,
CORS misconfiguration, API versioning issues, and lack of API monitoring.
Provide API-specific security recommendations.""",

        "compliance_checker": """You are a compliance and security auditor.
Check for compliance with: GDPR, PCI-DSS, HIPAA, SOC2, ISO 27001.
Identify: data handling issues, logging/audit trail gaps, encryption requirements,
access control problems, incident response readiness.
Rate findings by compliance impact.""",

        "developer_focused": """You are a security-conscious developer helping other developers improve security.
Provide security recommendations that are: practical to implement, not overly complex,
focused on common mistakes, include code examples where applicable.
Explain the 'why' behind each recommendation to help developers learn.""",

        "pentest_report": """You are writing a penetration test report for stakeholders.
Be: professional, clear, business-focused. Explain findings in terms of business impact.
Structure findings by: severity, affected systems, business risk, remediation steps, timeline.
Avoid overly technical language; make it understandable to non-technical executives.""",
    }

    def __init__(self):
        """Initialize prompt manager"""
        self.prompts_dir = self.PROMPTS_DIR
        self.prompts_dir.mkdir(exist_ok=True)
        self._load_default_prompts()

    def _load_default_prompts(self):
        """Load default prompts to disk if not present"""
        for name, content in self.DEFAULT_PROMPTS.items():
            prompt_file = self.prompts_dir / f"{name}.txt"
            if not prompt_file.exists():
                prompt_file.write_text(content)

    def get_prompt(self, name: str) -> str:
        """Get a system prompt by name"""
        prompt_file = self.prompts_dir / f"{name}.txt"
        
        if prompt_file.exists():
            return prompt_file.read_text()
        
        # Return built-in default
        if name in self.DEFAULT_PROMPTS:
            return self.DEFAULT_PROMPTS[name]
        
        # Return generic default
        return self.DEFAULT_PROMPTS.get("security_analyzer",
            "You are a security analyst. Analyze the provided traffic for security issues.")

    def list_prompts(self) -> List[str]:
        """List all available prompts"""
        prompts = list(self.DEFAULT_PROMPTS.keys())
        
        # Add custom prompts from disk
        if self.prompts_dir.exists():
            for prompt_file in self.prompts_dir.glob("*.txt"):
                name = prompt_file.stem
                if name not in prompts:
                    prompts.append(name)
        
        return sorted(prompts)

    def save_custom_prompt(self, name: str, content: str) -> bool:
        """Save a custom system prompt"""
        try:
            prompt_file = self.prompts_dir / f"{name}.txt"
            prompt_file.write_text(content)
            return True
        except Exception as e:
            print(f"Error saving prompt: {e}")
            return False

    def delete_prompt(self, name: str) -> bool:
        """Delete a custom prompt"""
        try:
            # Don't delete built-in prompts
            if name in self.DEFAULT_PROMPTS:
                return False
            
            prompt_file = self.prompts_dir / f"{name}.txt"
            if prompt_file.exists():
                prompt_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting prompt: {e}")
            return False

    def get_prompt_description(self, name: str) -> str:
        """Get description of what a prompt does"""
        descriptions = {
            "security_analyzer": "General security analysis and vulnerability detection",
            "owasp_expert": "OWASP Top 10 focused security assessment",
            "api_security": "API-specific security analysis and recommendations",
            "compliance_checker": "Compliance and regulatory requirement checks",
            "developer_focused": "Developer-friendly security guidance",
            "pentest_report": "Professional penetration test reporting format",
        }
        return descriptions.get(name, "Custom security analysis prompt")

    def export_prompt(self, name: str, output_file: str) -> bool:
        """Export prompt to a file"""
        try:
            content = self.get_prompt(name)
            Path(output_file).write_text(content)
            return True
        except Exception as e:
            print(f"Error exporting prompt: {e}")
            return False

    def import_prompt(self, name: str, input_file: str) -> bool:
        """Import prompt from a file"""
        try:
            content = Path(input_file).read_text()
            return self.save_custom_prompt(name, content)
        except Exception as e:
            print(f"Error importing prompt: {e}")
            return False

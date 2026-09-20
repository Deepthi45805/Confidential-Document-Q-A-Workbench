import json
import requests
from typing import Dict, Any, Optional
from config.settings import EXECUTION_MODE, OLLAMA_BASE_URL, OLLAMA_MODEL

class LLMService:
    def __init__(self, mode: str = EXECUTION_MODE):
        self.mode = mode
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if self.mode == "DEMO":
            return self._demo_fallback_generate(prompt)

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            if system_prompt:
                payload["system"] = system_prompt

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"[Fallback Demo Mode Triggered] Ollama HTTP {response.status_code}. Unable to communicate with local model."
        except Exception as e:
            return self._demo_fallback_generate(prompt)

    def _demo_fallback_generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "route this query" in prompt_lower or "classify" in prompt_lower:
            if "summar" in prompt_lower:
                return json.dumps({
                    "agent": "SUMMARIZER",
                    "reason": "Request contains summarization keywords."
                })
            elif "compare" in prompt_lower or "changed" in prompt_lower or "difference" in prompt_lower:
                return json.dumps({
                    "agent": "COMPARATOR",
                    "reason": "Request asks for comparison between document versions."
                })
            else:
                return json.dumps({
                    "agent": "QA",
                    "reason": "Request is a direct factual query seeking specific information."
                })

        if "summarize" in prompt_lower or "summary" in prompt_lower:
            return """### Executive Summary
This document outlines core operational procedures, standards, and institutional frameworks.

### Key Points
- Establishes standardized guidelines across organizational workflows.
- Defines clear responsibilities for team members and management.
- Sets protocol thresholds for compliance, privacy, and local data security.

### Important Details
- All activities must adhere strictly to local compliance guidelines.
- Standard working hours and Leave Entitlements are updated annually.
- Data retention policies dictate all document access must be logged locally.

### Action Items
1. Review policy updates bi-annually.
2. Complete mandatory training modules within 30 days of release.
3. Report any security discrepancies directly to the administrator.

### Important Dates
- Effective Date: January 1, 2026
- Mandatory Annual Review: December 15, 2026

### Key Terms
- **Local Autonomy**: Processing data entirely on-premise without cloud transfers.
- **Audit Trail**: Non-repudiable local logging of document interactions."""

        return "Based on the retrieved context from the uploaded documents, the policy mandates strict local processing, clear organizational roles, and formal review schedules."

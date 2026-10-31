"""Provider-agnostic LLM client interface and implementations.

Provides:
- LLMClient (abstract base class)
- MockLLMClient (deterministic offline mock for tests and reproducible runs)
- OllamaLLMClient (local open-weight models via Ollama REST API)
- OpenAICompatibleLLMClient (generic OpenAI-compatible HTTP endpoints)
- Factory function get_llm_client()
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM completion providers."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generate a response text given prompt and optional system instructions."""
        pass


class MockLLMClient(LLMClient):
    """Deterministic offline mock LLM client for testing and offline evaluation.

    Produces structured, guideline-grounded responses without network access.
    """

    def __init__(self, model_name: str = "mock-clinical-v1") -> None:
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Deterministically format a clinical response based on prompt context."""
        lower = prompt.lower()

        # Check for abstention / out-of-scope triggers
        if "out-of-scope" in lower or "out of scope" in lower or "pediatric asthma" in lower:
            return (
                "### Clinical Decision Support Notice: Out-of-Scope Query\n\n"
                "**Guideline Scope Limitation**: This decision support system is strictly designed "
                "for adult Hypertension and Type 2 Diabetes guideline management (MoHFW STG 2016, "
                "ICMR STW, WHO HEARTS/Hypertension/HEARTS-D, NICE NG136/NG28).\n\n"
                "The requested condition or question falls outside this clinical corpus. "
                "No recommendations can be safely generated. Please consult appropriate clinical "
                "specialists or pediatric treatment guidelines directly.\n\n"
                "*Research Prototype Disclaimer: For evaluation and research purposes only.*"
            )

        # Check for contradiction / clarify triggers
        if "disputed claims detected" in lower or "contradiction detected" in lower:
            return (
                "### Clarification Required: Conflicting Patient Information\n\n"
                "**Clinical Ambiguity Detected**: A direct conflict was identified in the patient history:\n"
                "- A previous assertion contradicts the newly reported clinical status.\n\n"
                "Before initiating or modifying pharmacotherapy, please confirm the correct patient history "
                "and current clinical readings to ensure guideline safety.\n\n"
                "*Research Prototype Disclaimer: For evaluation and research purposes only.*"
            )

        # Check for pushback triggers
        if "pushback" in lower or "patient refuses" in lower or "doubts medication" in lower:
            return (
                "### Guideline Treatment Rationale: Response to Patient Concern\n\n"
                "**Clinical Guideline Rationale**: While lifestyle modifications (reduced dietary sodium, "
                "weight optimization, regular physical exercise) form the foundation of cardiovascular risk reduction, "
                "guideline evidence consistently demonstrates that confirmed sustained hypertension (SBP ≥ 140 or DBP ≥ 90 mmHg) "
                "requires pharmacotherapy in conjunction with lifestyle interventions to prevent long-term target organ damage.\n\n"
                "Lifestyle modifications alone are insufficient when blood pressure remains persistently elevated above threshold. "
                "Initial pharmacotherapy with an ACE inhibitor, ARB, CCB, or thiazide-like diuretic is strongly advised.\n\n"
                "*Research Prototype Disclaimer: For evaluation and research purposes only.*"
            )

        # Default fallback mock response
        return (
            "### Clinical Guideline Recommendation\n\n"
            "Based on established clinical guidelines, initial pharmacotherapy should be selected based on "
            "patient age, ethnicity, and comorbidities (e.g., CKD, Type 2 Diabetes).\n\n"
            "*Research Prototype Disclaimer: For evaluation and research purposes only.*"
        )


class OllamaLLMClient(LLMClient):
    """Local open-weight LLM client connecting to Ollama HTTP API."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1:8b",
        temperature: float = 0.0,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Call Ollama /api/generate endpoint."""
        url = f"{self.base_url}/api/generate"
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        if system_prompt:
            payload["system"] = system_prompt

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                return str(result.get("response", ""))
        except (urllib.error.URLError, TimeoutError) as exc:
            logger.error("Ollama connection failed: %s", exc)
            raise ConnectionError(f"Failed to connect to Ollama at {self.base_url}: {exc}") from exc


class OpenAICompatibleLLMClient(LLMClient):
    """Client for any OpenAI-compatible chat completions endpoint."""

    def __init__(
        self,
        base_url: str = "https://api.openai.com/v1",
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.model = model
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Call /chat/completions endpoint."""
        url = f"{self.base_url}/chat/completions"
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }

        req_data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                choices = result.get("choices", [])
                if choices:
                    return str(choices[0].get("message", {}).get("content", ""))
                return ""
        except (urllib.error.URLError, TimeoutError) as exc:
            logger.error("OpenAI-compatible endpoint failed: %s", exc)
            raise ConnectionError(
                f"Failed to connect to endpoint at {self.base_url}: {exc}"
            ) from exc


def get_llm_client(provider: str | None = None, **kwargs: Any) -> LLMClient:
    """Factory creating an LLMClient instance based on configuration."""
    resolved_provider = provider or os.getenv("LLM_PROVIDER", "mock").lower()

    if resolved_provider == "mock":
        return MockLLMClient(model_name=str(kwargs.get("model", "mock-clinical-v1")))
    elif resolved_provider == "ollama":
        return OllamaLLMClient(
            base_url=str(
                kwargs.get("base_url") or os.getenv("LLM_BASE_URL") or "http://localhost:11434"
            ),
            model=str(kwargs.get("model") or os.getenv("LLM_MODEL") or "llama3.1:8b"),
            temperature=float(kwargs.get("temperature", os.getenv("LLM_TEMPERATURE", "0.0"))),
        )
    elif resolved_provider in {"openai", "openai_compatible"}:
        return OpenAICompatibleLLMClient(
            base_url=str(
                kwargs.get("base_url") or os.getenv("LLM_BASE_URL") or "https://api.openai.com/v1"
            ),
            api_key=str(kwargs.get("api_key") or os.getenv("LLM_API_KEY") or ""),
            model=str(kwargs.get("model") or os.getenv("LLM_MODEL") or "gpt-4o-mini"),
            temperature=float(kwargs.get("temperature", os.getenv("LLM_TEMPERATURE", "0.0"))),
        )
    else:
        logger.warning(
            "Unrecognized LLM provider '%s'. Defaulting to MockLLMClient.", resolved_provider
        )
        return MockLLMClient()

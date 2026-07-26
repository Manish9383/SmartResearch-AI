import json
import os
from typing import Dict, Any, Type, Optional
from pydantic import BaseModel
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.logging import logger

class BaseAIAgent:
    """
    Base class for all specialized equity research AI agents.
    Handles Gemini API invocation with strict schema outputs and graceful fallback execution.
    """

    def __init__(self, agent_name: str, response_schema: Optional[Type[BaseModel]] = None):
        self.agent_name = agent_name
        self.response_schema = response_schema

    def _get_gemini_client(self) -> Optional[genai.Client]:
        api_key = (settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")).strip()
        if api_key:
            return genai.Client(api_key=api_key)
        return None

    def execute_prompt(
        self,
        system_instruction: str,
        user_prompt: str,
        temperature: float = 0.1
    ) -> Optional[Dict[str, Any]]:
        client = self._get_gemini_client()
        if not client:
            logger.info(f"[{self.agent_name}] Gemini API key missing. Returning None to trigger heuristic fallback.")
            return None

        candidate_models = [settings.DEFAULT_LLM_MODEL, "gemini-2.5-flash", "gemini-2.0-flash"]
        unique_models = []
        for m in candidate_models:
            if m not in unique_models:
                unique_models.append(m)

        import time
        for model_name in unique_models:
            try:
                logger.info(f"[{self.agent_name}] Invoking model {model_name}...")
                config_kwargs = {
                    "system_instruction": system_instruction,
                    "temperature": temperature,
                }
                if self.response_schema:
                    config_kwargs["response_mime_type"] = "application/json"
                    config_kwargs["response_schema"] = self.response_schema

                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(**config_kwargs)
                )

                if response.text:
                    if self.response_schema or response.text.strip().startswith("{"):
                        return json.loads(response.text)
                    return {"raw_text": response.text}

            except Exception as e:
                err_str = str(e)
                logger.warning(f"[{self.agent_name}] Model {model_name} error: {err_str}")
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    time.sleep(2)  # Brief wait for free-tier rate limit resets

        logger.error(f"[{self.agent_name}] All Gemini models failed. Triggering heuristic fallback.")
        return None

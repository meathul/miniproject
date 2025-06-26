from langchain.llms.base import LLM
from groq import Groq
from typing import Optional, List
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class GroqLLM(LLM):
    model: str = Field(default="llama3-8b-8192")
    temperature: float = Field(default=0.0)
    api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        client = Groq(api_key=self.api_key)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        return "groq-llm" 
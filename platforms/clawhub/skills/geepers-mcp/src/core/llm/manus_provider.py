"""
Manus AI provider implementation.
Supports Manus agent profiles with task-based asynchronous processing.
"""

from typing import List, Dict, Any, Union
from . import BaseLLMProvider, Message, CompletionResponse
import os
import time
import requests


class ManusProvider(BaseLLMProvider):
    """Manus AI provider using task-based API."""

    DEFAULT_MODEL = "manus-1.5"
    BASE_URL = "https://api.manus.ai/v1"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("MANUS_API_KEY")
        if not api_key:
            raise ValueError("MANUS_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        self.headers = {
            "API_KEY": api_key,
            "Content-Type": "application/json"
        }

    def _create_task(self, prompt: str, agent_profile: str, task_mode: str = "chat", attachments: List[Dict] = None) -> str:
        """Create a new task and return task_id."""
        payload = {
            "prompt": prompt,
            "agentProfile": agent_profile,
            "taskMode": task_mode
        }

        if attachments:
            payload["attachments"] = attachments

        response = requests.post(
            f"{self.BASE_URL}/tasks",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        return data["task_id"]

    def _get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status and output."""
        response = requests.get(
            f"{self.BASE_URL}/tasks/{task_id}",
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def _wait_for_completion(self, task_id: str, poll_interval: float = 2.0, max_wait: int = 300) -> Dict[str, Any]:
        """Poll task until completion or timeout."""
        start_time = time.time()

        while True:
            if time.time() - start_time > max_wait:
                raise TimeoutError(f"Task {task_id} did not complete within {max_wait} seconds")

            task_data = self._get_task_status(task_id)
            status = task_data.get("status")

            if status == "completed":
                return task_data
            elif status == "failed":
                error_msg = task_data.get("error", "Unknown error")
                raise Exception(f"Task failed: {error_msg}")

            # Status is "pending" or "running", continue polling
            time.sleep(poll_interval)

    def _extract_response_text(self, task_data: Dict[str, Any]) -> str:
        """Extract the assistant's response text from task output."""
        output = task_data.get("output", [])

        # Find assistant messages with output_text
        for message in output:
            if message.get("role") == "assistant":
                content = message.get("content", [])
                for item in content:
                    if item.get("type") == "output_text":
                        return item.get("text", "")

        return ""

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Manus agent."""
        # Convert message history to a single prompt
        # Manus uses a task-based system, so we concatenate the conversation
        prompt_parts = []
        for msg in messages:
            if msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")

        # Use the last user message as the main prompt if available
        if messages and messages[-1].role == "user":
            prompt = messages[-1].content
        else:
            prompt = "\n\n".join(prompt_parts)

        # Get model/agent profile from kwargs or use instance default
        agent_profile = kwargs.get("model", self.model)
        task_mode = kwargs.get("task_mode", "chat")
        max_wait = kwargs.get("max_wait", 300)  # 5 minutes default

        # Create task
        task_id = self._create_task(prompt, agent_profile, task_mode)

        # Wait for completion
        task_data = self._wait_for_completion(task_id, max_wait=max_wait)

        # Extract response
        content = self._extract_response_text(task_data)

        # Calculate token usage (Manus returns credit_usage)
        credit_usage = task_data.get("credit_usage", 0)

        return CompletionResponse(
            content=content,
            model=task_data.get("model", agent_profile),
            usage={
                "prompt_tokens": 0,  # Manus doesn't provide token breakdown
                "completion_tokens": 0,
                "total_tokens": 0,
                "credit_usage": credit_usage
            },
            metadata={
                "task_id": task_id,
                "task_url": task_data.get("task_url"),
                "created_at": task_data.get("created_at"),
                "updated_at": task_data.get("updated_at")
            }
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """
        Stream a completion using Manus.

        Note: Manus doesn't support true streaming. This method polls the task
        and yields the complete response once available.
        """
        # Create the task
        prompt_parts = []
        for msg in messages:
            if msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")

        if messages and messages[-1].role == "user":
            prompt = messages[-1].content
        else:
            prompt = "\n\n".join(prompt_parts)

        agent_profile = kwargs.get("model", self.model)
        task_mode = kwargs.get("task_mode", "chat")

        task_id = self._create_task(prompt, agent_profile, task_mode)

        # Poll until completion and yield the result
        task_data = self._wait_for_completion(task_id)
        content = self._extract_response_text(task_data)

        # Yield the complete response (simulated streaming)
        yield content

    def list_models(self) -> List[str]:
        """List available Manus agent profiles."""
        return [
            "manus-1.5",
            "manus-1.5-lite",
            "speed",
            "quality"
        ]

    def analyze_image(self, image: Union[str, bytes], prompt: str = "Describe this image", **kwargs) -> CompletionResponse:
        """
        Analyze an image using Manus agent.

        Args:
            image: Base64-encoded string or raw bytes
            prompt: Question about the image
            **kwargs: Optional parameters
                - model: Agent profile (default: self.model)
                - task_mode: Task mode (default: "chat")

        Returns:
            CompletionResponse with image analysis
        """
        import base64

        # Convert bytes to base64 if needed
        if isinstance(image, bytes):
            image_b64 = base64.b64encode(image).decode('utf-8')
        else:
            image_b64 = image

        # Create attachment for the image
        attachments = [{
            "type": "image",
            "data": image_b64
        }]

        agent_profile = kwargs.get("model", self.model)
        task_mode = kwargs.get("task_mode", "chat")
        max_wait = kwargs.get("max_wait", 300)

        # Create task with image attachment
        task_id = self._create_task(prompt, agent_profile, task_mode, attachments)

        # Wait for completion
        task_data = self._wait_for_completion(task_id, max_wait=max_wait)

        # Extract response
        content = self._extract_response_text(task_data)
        credit_usage = task_data.get("credit_usage", 0)

        return CompletionResponse(
            content=content,
            model=task_data.get("model", agent_profile),
            usage={
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "credit_usage": credit_usage
            },
            metadata={
                "task_id": task_id,
                "task_url": task_data.get("task_url"),
                "vision": True
            }
        )

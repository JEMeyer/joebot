import asyncio
import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam


class LLMClient:
    """Client for communicating with LLM APIs."""

    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        """Initialize the LLM client.

        Args:
            api_key: API key for the LLM provider
            model: Model identifier to use
            base_url: Base URL for the LLM provider's API
        """
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.model: str = model
        self.timeout: float = 30.0  # 30 second timeout
        self.max_retries: int = 2
        self.client: AsyncOpenAI = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    async def get_response(self, messages: list[ChatCompletionMessageParam]) -> str:
        """Get a response from the LLM API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            The LLM's response as a string
        """
        return await self._get_openai_response(messages)

    async def _get_openai_response(
        self, messages: list[ChatCompletionMessageParam]
    ) -> str:
        """Get a response from the OpenAI API."""
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                )

                message_content = response.choices[0].message.content or ""
                return message_content
            except Exception as e:
                if attempt == self.max_retries:
                    return f"Failed to get response: {str(e)}"
                await asyncio.sleep(
                    2**attempt  # pyright: ignore[reportAny]
                )  # Exponential backoff
        return "Failed to get response -- end of function"

    async def interpret_tool_result(
        self, tool_name: str, arguments: str, tool_result: str
    ) -> str:
        """Get an interpretation of a tool result from the LLM.

        Args:
            tool_name: Name of the tool that was executed
            arguments: Arguments that were passed to the tool
            tool_result: Result returned by the tool

        Returns:
            LLM's interpretation of the tool result
        """
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful record keeper. When you receive "
                    "a result from a tool as reported by the user, "
                    "interpret these results in a clear, helpful way, "
                    "which may mean no modification to the result."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"I used the tool {tool_name} with arguments "
                    f"{arguments} and got this result:\n\n"
                    f"{tool_result}\n\n"
                    f"Please interpret this result for me."
                ),
            },
        ]

        try:
            return await self.get_response(messages)
        except Exception as e:
            logging.error(
                f"Error getting tool result interpretation: {e}", exc_info=True
            )
            raise


from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        prompt: str
    ) -> dict:
        """
        Generate a response using the configured LLM provider.

        Args:
            prompt: Input prompt.

        Returns:
            A dictionary containing:
            - provider: Provider name.
            - model: Model name.
            - response: Generated text.
        """
        pass

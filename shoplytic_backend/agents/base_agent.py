from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseAgent(ABC):
    """Tüm AI agent'lar için abstract base class."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, input_data: Any, context: Optional[dict] = None) -> Any:
        """Agent'ı çalıştır."""
        ...

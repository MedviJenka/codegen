from typing import Optional
from crewai import Agent, Task
from abc import ABC, abstractmethod
from agent_ops.src.utils.azure_llm import AzureLLMConfig


class AgentInfrastructure(ABC, AzureLLMConfig):

    def __init__(self, debug: Optional[bool] = True) -> None:
        super().__init__()
        self.debug = debug
        self.agents: list[Agent] = []
        self.tasks: list[Task] = []
        self.agents_config: callable = "config/agents.yaml"
        self.tasks_config: callable = "config/tasks.yaml"

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> None: ...

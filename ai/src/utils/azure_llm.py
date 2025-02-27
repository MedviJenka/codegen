import os
from crewai import LLM
from functools import cached_property
from crewai.telemetry import Telemetry


class TelemetryPatch:

    def __init__(self) -> None:
        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, self.__noop)

    def __noop(*args: any, **kwargs: any) -> None:
        """dummy function for handling telemetry"""
        pass


class AzureLLMConfig(TelemetryPatch):

    @cached_property
    def llm(self) -> LLM:
        return LLM(model=os.getenv('MODEL'), api_version=os.getenv('AZURE_API_VERSION'), temperature=0)

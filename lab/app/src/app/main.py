import asyncio
from crewai import Flow
from crewai.flow.flow import start, listen
from pydantic import BaseModel
from lab.app.src.app.functions_map_crew import FunctionMapCrew
from lab.app.src.app.test_plan_crew import TestPlanCrew
from src.core.paths import TEST_PLAN


class InitialState(BaseModel):
    cache: str = ""


class Main(Flow[InitialState]):

    @start()
    def read_the_test_plan(self) -> None:
        read_test_plan = lambda path: open(path, "r", encoding="utf-8").read()
        result = TestPlanCrew().crew().kickoff(inputs={'test_plan': read_test_plan(TEST_PLAN)})
        self.state.cache = result.raw

    @listen(read_the_test_plan)
    def get_asterisk(self) -> None:
        print(self.state.cache)
        print("Asterisk: ", self.state.cache.count("*"))

    @listen(get_asterisk)
    def functions_mapping(self) -> None:
        function_crew = FunctionMapCrew().crew().kickoff()
        self.state.cache = function_crew


async def run_flow() -> None:
    flow = Main()
    await flow.kickoff_async()  # ✅ Use `kickoff_async()` instead of `kickoff()` to avoid `asyncio.run()`


async def plot_flow() -> None:
    flow = Main()
    flow.plot()


async def main() -> None:
    await run_flow()  # ✅ Await the function directly inside an async event loop


def plot() -> None:
    asyncio.run(plot_flow())  # Still safe since plotting is not inside an event loop


if __name__ == "__main__":
    asyncio.run(main())  # ✅ Now correctly runs inside the main event loop

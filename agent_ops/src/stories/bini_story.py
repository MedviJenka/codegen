from crewai import Flow
from crewai.flow import start, listen, router
from pydantic import BaseModel
from agent_ops.src.team.bini.crew import Bini
from agent_ops.src.team.english_professor.crew import EnglishProfessor


IMAGE = r'C:\Users\evgenyp\PycharmProjects\codegen\agent_ops\src\team\bini\img.png'


class InitialState(BaseModel):
    cache: str = ""


class BiniOps(Flow[InitialState]):

    @start()
    def refactor_prompt_to_valid_english(self, prompt: str) -> None:
        result = EnglishProfessor().execute(prompt=prompt)
        self.state.cache = result.raw

    # @listen(refactor_prompt_to_valid_english)
    # def run_bini(self, image_path: str) -> None:
    #     result = Bini().execute(prompt=self.state.cache, image_path=image_path)
    #     self.state.cache = result.raw
    #
    # @router(run_bini)
    # def decision_point_1(self) -> str:
    #     if self.state.cache == "Passed":
    #         return 'Success'
    #     return 'Failed'
    #
    # @listen('Success')
    # def success(self) -> None:
    #     print("Success")
    #
    # @listen('Failed')
    # def failed(self) -> None:
    #     print('Failed')


def execute(prompt, image) -> None:
    ops = BiniOps()
    ops.kickoff(inputs={'prompt': prompt, 'image': image})

execute("This is a test", IMAGE)

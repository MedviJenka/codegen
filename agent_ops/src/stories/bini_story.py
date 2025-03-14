from crewai import Flow
from crewai.flow import start, listen, router
from pydantic import BaseModel
from agent_ops.src.team.bini.crew import Bini
from agent_ops.src.team.english_professor.crew import EnglishProfessor


IMAGE = r'C:\Users\evgenyp\PycharmProjects\codegen\agent_ops\src\team\bini\img.png'


class InitialState(BaseModel):
    cache: str = ""
    prompt: str = ""
    image: str = ""


class BiniOps(Flow[InitialState]):

    @start()
    def refactor_prompt_to_valid_english(self) -> None:
        result = EnglishProfessor().execute(prompt=self.state.prompt)
        self.state.cache = result.raw

    @listen(refactor_prompt_to_valid_english)
    def run_bini(self) -> None:
        result = Bini().execute(prompt=self.state.cache, image_path=self.state.image)
        self.state.cache = result.raw

    @router(run_bini)
    def decision_point_1(self) -> str:
        return 'Success' if self.state.cache == "Passed" else 'Failed'

    @listen('Success')
    def success(self) -> None:
        print("Success")

    @listen('Failed')
    def failed(self) -> None:
        print('Failed')


def execute(prompt, image) -> None:
    BiniOps().kickoff(inputs={'prompt': prompt, 'image': image})


execute("This is a test", IMAGE)

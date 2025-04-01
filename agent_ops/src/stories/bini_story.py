from crewai import Flow
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, Union
from crewai.flow import start, listen, router
from agent_ops.src.team.bini.crew import ComputerVisionAgent
from agent_ops.src.team.chain_of_thought.crew import ChainOfThought
from agent_ops.src.team.english_professor.crew import EnglishProfessor
from agent_ops.src.team.validation_agent.crew import ValidationAgent
from event_recorder.core.paths import MAIN_IMAGE, SAMPLE_IMAGE_1, SAMPLE_IMAGE_2


class InitialState(BaseModel):
    prompt: str = ''
    image: str = ''
    sample_image: Union[str, list, None] = ''
    data: str = ''
    result: str = ''


class BiniOps(Flow[InitialState]):

    @start()
    def refine_prompt(self) -> None:
        self.state.prompt = EnglishProfessor().execute(prompt=self.state.prompt)

    @listen(refine_prompt)
    def analyze_image(self) -> None:
        self.state.data = ComputerVisionAgent().execute(prompt=self.state.prompt, image_path=self.state.image)

    @listen(analyze_image)
    def think_through(self) -> None:
        self.state.data = ChainOfThought().execute(prompt=self.state.data)

    @listen(think_through)
    def validate_result(self) -> None:
        self.state.data = ValidationAgent().execute(data=self.state.data)

    # ------------------------------------------------------------------------------------------------------------------

    @router(validate_result)
    def decision_point(self) -> str:
        """meaning: if self.state.data == 'Passed' then return 'Passed' else return 'Failed'"""
        self.state.result = self.state.data
        return self.state.result

    # ------------------------------------------------------------------------------------------------------------------

    @listen('Passed')
    def on_success(self) -> str:
        return 'Passed, image was identified and the question was valid'

    @listen('Failed')
    def on_failure(self) -> str:
        return 'Failed, image could not be identified'

    @listen('Invalid Question')
    def on_invalid(self) -> str:
        return 'Invalid question was provided, please rephrase'


@dataclass
class BiniOpsUtils:

    flow = BiniOps()

    def execute(self, prompt: str, image: str, sample_image: Optional[Union[str, list]] = '') -> str:
        return self.flow.kickoff(inputs={'prompt': prompt, 'image': image, 'sample_image': sample_image})


def test() -> None:
    bini = BiniOpsUtils()
    result = bini.execute(prompt='does cat displayed in this image?',
                          image=MAIN_IMAGE,
                          sample_image=[SAMPLE_IMAGE_1, SAMPLE_IMAGE_2])
    assert 'Failed' in result

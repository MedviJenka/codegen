from crewai import Flow
from pydantic import BaseModel
from typing import Optional, Union
from dataclasses import dataclass
from crewai.flow import start, listen, router
from agent_ops.src.team.bini.crew import Bini
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
        self.state.data = EnglishProfessor().execute(prompt=self.state.prompt).raw

    @listen(refine_prompt)
    def analyze_image(self) -> None:
        self.state.data = Bini().execute(prompt=self.state.prompt, image_path=self.state.image).raw

    @listen(analyze_image)
    def think_through(self) -> None:
        steps = ChainOfThought().execute(prompt=self.state.data)
        self.state.data = steps

    @listen(think_through)
    def validate_result(self) -> None:
        self.state.data = ValidationAgent().execute(data=self.state.data)

    @router(validate_result)
    def decision_point_1(self) -> str:

        match self.state.data:
            case 'Passed':
                return self._set_result('Passed')
            case 'Failed':
                return self._set_result('Failed')
            case 'Invalid Question':
                return self._set_result('Invalid Question')
            case _:
                return self._set_result('Unhandled')

    def _set_result(self, status: str) -> str:
        self.state.result = status
        return status

    @listen('Passed')
    def on_success(self) -> str:
        return 'Passed'

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
        return self.flow.kickoff(inputs={
            'prompt': prompt,
            'image': image,
            'sample_image': sample_image
        })


def test() -> None:
    result = BiniOpsUtils().execute(
        prompt='Do the sample images appear in the main image?',
        image=MAIN_IMAGE,
        sample_image=[SAMPLE_IMAGE_1, SAMPLE_IMAGE_2]
    )
    assert 'Passed' in result

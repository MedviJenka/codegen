from typing import Optional
from crewai import Flow
from pydantic import BaseModel
from dataclasses import dataclass
from crewai.flow import start, listen, router
from agent_ops.src.team.bini.crew import Bini
from agent_ops.src.team.english_professor.crew import EnglishProfessor
from event_recorder.core.paths import MAIN_IMAGE, SAMPLE_IMAGE_1, SAMPLE_IMAGE_2


class InitialState(BaseModel):
    cache: str = ''
    image: str  = ''
    prompt: str = ''


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

        if 'Passed' in self.state.cache:
            return 'Success'
        elif 'Failed' in self.state.cache:
            return 'Failed'
        else:
            return 'Invalid Question'

    @listen('Success')
    def success(self) -> None:
        print('Success')

    @listen('Failed')
    def failed(self) -> None:
        print('Failed, image could not be identified')

    # @listen('Invalid Question')
    # def invalid(self) -> None:
    #     print('Invalid question was provided, please rephrase')


@dataclass
class BiniOpsUtils:

    bini = BiniOps()

    def execute(self, prompt: str, image: str, sample_image: Optional[str or list] = '') -> str:
        return self.bini.kickoff(inputs={'prompt': prompt, 'image': image, 'sample_image': sample_image})


if __name__ == '__main__':
    ops = BiniOpsUtils()
    ops.execute(prompt='does the sample images displayed in the main image?',
                image=MAIN_IMAGE,
                sample_image=[SAMPLE_IMAGE_1, SAMPLE_IMAGE_2])

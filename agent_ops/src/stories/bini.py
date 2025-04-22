import os
import uuid
import json
from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from crewai.flow import Flow, start, listen, router

from agent_ops.src.agents.computer_vision.crew import ComputerVisionAgent
from agent_ops.src.agents.english_agent.crew import EnglishAgent
from src.core.paths import GLOBAL_PATH


class InitialState(BaseModel):

    """
    1. the flow starts with initial question aka prompt
    2. image and an optional sample image should be passed
    3. data stores all the results and passes from crew to crew
    4. result is the final answer which is passed / failed
    5. cache is used to store all the results in valid json file
    """

    prompt: str = ''
    image: str = ''
    sample_image: Union[str, list, None] = ''
    data: str = ''
    result: str = ''
    cache: dict = Field(default_factory=dict)


class BiniOps(Flow[InitialState]):

    """
    TODO: add logs
    BiniOps is a class that defines a flow for processing an image and a prompt.
    1. refines the prompt using an English professor agent.
    2. analyzes the image using a computer vision agent.
    3. thinks through the data using a chain of thought agent.
    4. decides the final result based on the validation.

    """

    def __init__(self, debug: Optional[bool] = False) -> None:
        self.debug = debug
        self.english_agent = EnglishAgent(debug=self.debug)
        self.computer_vision_agent = ComputerVisionAgent(debug=self.debug)
        super().__init__()

    @start()
    def refine_prompt(self) -> None:
        self.state.cache['date'] = datetime.now().strftime("%d/%m/%Y at %H:%M")
        self.state.prompt = self.english_agent.execute(prompt=self.state.prompt)
        self.state.cache['refined_prompt'] = self.state.prompt

    @listen(refine_prompt)
    def analyze_image(self) -> None:
        self.state.data = self.computer_vision_agent.execute(prompt=self.state.prompt,
                                                             image_path=self.state.image,
                                                             sample_image=self.state.sample_image)
        self.state.cache['image_data'] = self.state.data

    # ------------------------------------------------------------------------------------------------------------------

    @router(analyze_image)
    def decision_point(self) -> str:
        """meaning: if self.state.data == 'Passed' then result = 'Passed' else return 'Failed'"""
        if 'Passed' in self.state.data:
            self.state.result = 'Passed'
        elif 'Failed' in self.state.data:
            self.state.result = 'Failed'
        return self.state.result

    # ------------------------------------------------------------------------------------------------------------------

    @listen('Passed')
    def on_success(self) -> None:
        self.state.cache['result'] = 'Passed'

    @listen('Failed')
    def on_failure(self) -> None:
        self.state.cache['result'] = 'Failed'

    @listen('Invalid Question')
    def on_invalid(self) -> None:
        self.state.cache['result'] = 'Invalid Question was provided'

    def flow_to_json(self) -> dict:
        results_dir = fr'{GLOBAL_PATH}\qasharedinfra\infra\common\services\agent_ops\results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        json_path = fr'{results_dir}\bini-{__name__}.json-{uuid.uuid4()}'
        with open(json_path, 'w') as file:
            json.dump(self.state.cache, file, indent=4)
        return self.state.cache

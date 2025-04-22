from pathlib import Path
from typing import Optional
from agent_ops.src.stories.bini import BiniOps


class BiniOpsUtils:

    """
    TODO:
        Question 1: do we want as_dict to be a constructor argument or a function argument?
    """

    def __init__(self, debug: Optional[bool] = True) -> None:
        self.debug = debug
        self.bini_ops = BiniOps(debug=self.debug)

    def run(self,
            prompt: str,
            image_path: str,
            sample_image: Optional[list[str]] = '',
            as_dict: Optional[bool] = False,
            delete_image: Optional[bool] = False) -> dict:

        if isinstance(image_path, Path):
            image = Path(image_path).as_posix()
            if delete_image and Path(image_path).exists():
                Path.unlink(image)

        self.bini_ops.kickoff(inputs={'prompt': prompt, 'image': image_path, 'sample_image': sample_image})

        if as_dict:
            return self.bini_ops.flow_to_json()

        return self.bini_ops.flow_to_json().get('result')

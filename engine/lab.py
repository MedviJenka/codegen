from bini_ai.infrastructure.constants import IMAGE_1
from bini_ai.infrastructure.utils import BiniUtils


bini = BiniUtils()


print(bini.run_image_processing(image_path=IMAGE_1, prompt=''))

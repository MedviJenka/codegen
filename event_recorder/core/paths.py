import os

# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Global project path
GLOBAL_PATH: str = abstract_dir.split('event_recorder')[0][:-1]

# Common paths
LOG = fr'{GLOBAL_PATH}\output\code_gen.log'
PAGE_BASE = fr'{GLOBAL_PATH}\output\page_base.csv'
FUNCTIONS_INDEX = fr'{GLOBAL_PATH}\functions'
TEST_PLAN = rf'{GLOBAL_PATH}\tests\test_plan.md'
FUNCTION = fr'{GLOBAL_PATH}\functions'
AI_PAGE_BASE = fr'{GLOBAL_PATH}\output\ai_page_base.csv'
AI_PYTHON_CODE = fr'{GLOBAL_PATH}\output\ai_test_code.py'
PYTHON_CODE = fr'{GLOBAL_PATH}\output\test_code.py'
PYTHON_CODE_AI = fr'{GLOBAL_PATH}\output\test_code_ai.py'
OUTPUT_PATH = fr'{GLOBAL_PATH}\output'
JS_SCRIPT = fr'{GLOBAL_PATH}\event_recorder\engine\script.js'

MAIN_IMAGE = fr'{GLOBAL_PATH}\images\google_main.png'

SAMPLE_IMAGE_1 = fr'{GLOBAL_PATH}\images\google_sample_1.png'
SAMPLE_IMAGE_2 = fr'{GLOBAL_PATH}\images\google_sample_2.png'
SAMPLE_IMAGE_3 = fr'{GLOBAL_PATH}\images\google_sample_3.png'
SAMPLE_IMAGE_4 = fr'{GLOBAL_PATH}\images\google_sample_4.png'
SAMPLE_IMAGE_5 = fr'{GLOBAL_PATH}\images\google_sample_5.png'

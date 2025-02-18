import os


# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Automation
GLOBAL_PATH: str = abstract_dir.split('src')[0][:-1]
LOG = fr'{GLOBAL_PATH}\output\code_gen.log'
PAGE_BASE = fr'{GLOBAL_PATH}\output\page_base.csv'
FUNCTIONS_INDEX = fr'{GLOBAL_PATH}\functions'
TEST_PLAN = rf'{GLOBAL_PATH}\tests\test_plan.md'
FUNCTION = fr'{GLOBAL_PATH}\functions'
AI_PAGE_BASE = fr'{GLOBAL_PATH}\output\ai_page_base.csv'
AI_PYTHON_CODE = fr'{GLOBAL_PATH}\output\ai_test_code.py'
PYTHON_CODE = fr'{GLOBAL_PATH}\output\test_code.py'

import os


# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Automation
GLOBAL_PATH: str = abstract_dir.split('src')[0][:-1]
LOG = fr'{GLOBAL_PATH}\output\code_gen.log'
PAGE_BASE = fr'{GLOBAL_PATH}\output\page_base.csv'
PYTHON_CODE = fr'{GLOBAL_PATH}\output\test_code.py'
FUNCTIONS_INDEX = fr'{GLOBAL_PATH}\functions'
TEST_PLAN = rf'{GLOBAL_PATH}\tests\test_plan.md'

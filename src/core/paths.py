import os


# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Automation
GLOBAL_PATH = abstract_dir.split('core')[0][:-1]
LOG = fr'{GLOBAL_PATH}\output\code_gen.log'
PAGE_BASE = fr'{GLOBAL_PATH}\output\page_base.csv'
PYTHON_CODE = fr'{GLOBAL_PATH}\output\test_code.py'

# files
IMAGE_1 = fr'{GLOBAL_PATH}\images\img_1.png'
IMAGE_2 = fr'{GLOBAL_PATH}\images\img33.png'

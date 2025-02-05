from src.utils.ai_utils import BiniCodeUtils
from src.integration.ai_browser_sync import BiniBrowserRecorder


if __name__ == '__main__':
    utils = BiniCodeUtils()
    bini = BiniBrowserRecorder(bini=utils)
    bini.run_bini_recorder()

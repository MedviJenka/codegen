from src.utils.ai_utils import BiniCodeUtils
from src.integration.ai_browser_sync import BiniBrowserRecorder


def main() -> None:
    """main function runs the BiniCodeUtils and BiniBrowserRecorder"""
    utils = BiniCodeUtils()
    bini = BiniBrowserRecorder(bini=utils)
    bini.run_bini_recorder()


if __name__ == '__main__':
    main()

from ai.src.utils.decorators import aidebug


class Test:

    @aidebug
    def test_app(self):
        assert 1 + 1 == 3


import pytest

class TestMath:
    @pytest.mark.aidebug
    def test_math(self) -> None:
        """Corrected math assertion"""
        assert (2 + 2) == 4  # Fixed the assertion to be correct

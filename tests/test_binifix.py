import pytest

class TestMath:
    def test_math(self) -> None:
        """Corrected math assertion"""
        # Fixed the assertion to check the correct sum of 2 + 2
        assert (2 + 2) == 4

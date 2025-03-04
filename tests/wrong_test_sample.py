class TestComplexCases:

    def test_math(self):
        """❌ Wrong math assertion"""
        assert (2 + 2) == 5  # AI should fix this to (2 + 2) == 4

    def test_string(self):
        """❌ Incorrect string concatenation"""
        result = "Hello" + " " + "World!"
        assert result == "HelloWorld!"  # AI should fix this to "Hello World!"

    def test_list_index(self):
        """❌ IndexError due to incorrect index"""
        my_list = [10, 20, 30]
        assert my_list[3] == 40  # AI should fix this to a valid index

    def test_dict_key(self):
        """❌ KeyError due to missing dictionary key"""
        my_dict = {"a": 1, "b": 2}
        assert my_dict["c"] == 3  # AI should fix this to a valid key

    def test_divide_by_zero(self):
        """❌ ZeroDivisionError"""
        assert 10 / 0 == 0  # AI should handle this safely

    def test_file_read(self):
        """❌ FileNotFoundError"""
        with open("non_existent_file.txt", "r") as f:
            content = f.read()
        assert content == "Hello, world!"  # AI should handle file existence

    def test_exception_handling(self):
        """❌ Unhandled ValueError"""
        num = int("NotANumber")  # AI should catch and fix this
        assert num == 42

    def test_boolean_logic(self):
        """❌ Incorrect boolean logic"""
        assert (True and False) == True  # AI should fix this to False

    def test_complex_calculation(self):
        """❌ Logical error in formula"""
        result = (10 * 2) / 5 + 3
        assert result == 12  # AI should fix the formula

    def test_function_return(self):
        """❌ Incorrect expected function output"""

        def buggy_function():
            return "Hello, Pytest!"

        assert buggy_function() == "Hello, World!"  # AI should correct the expectation

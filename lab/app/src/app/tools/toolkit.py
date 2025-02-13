from lab.app.src.app.tools.custom_tool import FunctionMapping


class ToolKit(FunctionMapping):

    def find_relevant_functions(self) -> dict:
        return self.index_functions

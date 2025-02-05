from src.lab.python.src.python.crew import PythonCrew


class RunTestCrew(PythonCrew):

    def run(self, topic: str):
        inputs = {'topic': topic}
        self.crew().kickoff(inputs=inputs)

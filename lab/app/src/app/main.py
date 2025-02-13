import warnings
from lab.app.src.app.crew import App


warnings.filterwarnings(action="ignore", category=SyntaxWarning, module="pysbd")


def read_test_plan(file: str) -> str:
    with open(file, encoding='utf-8') as test:
        return test.read()


def run():
    """Run the crew."""
    inputs = {
        'topic': read_test_plan(file=r'C:\Users\medvi\PycharmProjects\codegen\tests\test_plan.md'),
        'output': 'your thoughts'
    }
    
    try:
        App().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


run()

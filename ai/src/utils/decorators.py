import traceback
import inspect
import re
import sys
from typing import Optional
from functools import wraps
from ai.src.crews.debug_crew.crew import DebugCrew


def aidebug(_object:Optional[any] = None) -> callable:
    """Decorator that wraps test functions & test classes, invokes DebugCrew on failure, and autocorrects code.

    - Works on **functions**: `@aidebug`
    - Works on **classes**: `@aidebug`
    - Supports usage with or without parentheses: `@aidebug()` and `@aidebug`
    """

    def function_decorator(func):
        """Decorator for individual test functions."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                error_trace = traceback.format_exc()
                print(f"Test failed in {func.__name__}. Triggering DebugCrew...\n{error_trace}")

                # Extract source code of the function
                original_code = inspect.getsource(func)

                # Debug and Fix Code via AI Agent
                debug_team = DebugCrew()
                fixed_code = debug_team.execute(error_trace, original_code)

                # Sanitize AI-generated code
                fixed_code = re.sub(r"```python\n?|```", "", fixed_code).strip()

                # Inject fixed function dynamically into the module's namespace
                exec(fixed_code, globals())

                # Retrieve the module where the function is defined
                module = sys.modules[func.__module__]

                # Prevent infinite loop: Ensure decorator does not wrap the function again
                corrected_func_name = func.__name__
                if corrected_func_name in globals():
                    corrected_func = globals()[corrected_func_name]
                    setattr(module, corrected_func_name, corrected_func)  # Replace function in module
                    print(f"Function {corrected_func_name} successfully updated.")

                raise RuntimeError(f"Test function '{func.__name__}' has been fixed. Please rerun pytest.")

        return wrapper

    def class_decorator(cls):
        """Decorator for classes: applies aidebug to all test methods."""
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and attr_name.startswith("test"):
                setattr(cls, attr_name, function_decorator(attr_value))
        return cls

    # If called without parentheses (@aidebug), determine if it's a function or class
    if _object:
        return function_decorator(_object) if callable(_object) else class_decorator(_object)

    # If called with parentheses (@aidebug()), return a decorator function
    return lambda x: function_decorator(x) if callable(x) else class_decorator(x)

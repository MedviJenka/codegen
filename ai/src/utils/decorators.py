import traceback
import inspect
import re
import sys
from typing import Callable, Type, Optional
from functools import wraps
from ai.src.crews.debug_crew.crew import DebugCrew


def aidebug(function: Optional[any] = None) -> Callable:
    """Decorator that wraps test functions & test classes, invokes DebugCrew on failure, and autocorrects code.

    - Works on **functions**: `@aidebug`
    - Works on **classes**: `@aidebug`
    - Supports usage with or without parentheses: `@aidebug()` and `@aidebug`
    """

    def function_decorator(func: any) -> Callable:
        """Decorator for individual test functions that replaces the function but does NOT execute it."""

        @wraps(func)
        def wrapper(*args: any, **kwargs: any) -> None:
            try:
                return func(*args, **kwargs)

            except Exception as e:
                error_trace = traceback.format_exc()
                print(f"Test failed in {func.__name__}. Triggering DebugCrew...\n{error_trace}, error: {e}")

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

                return

        return wrapper

    def class_decorator(cls: Type) -> Type:
        """Decorator for classes: applies aidebug to all test methods but does NOT run them."""
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and attr_name.startswith("test"):
                setattr(cls, attr_name, function_decorator(attr_value))

        return cls  # ✅ Explicitly return the modified class to keep pytest compatibility

    # If called without parentheses (@aidebug), determine if it's a function or class
    if function:
        return function_decorator(function) if callable(function) else class_decorator(function)

    # If called with parentheses (@aidebug()), return a decorator function
    return lambda x: function_decorator(x) if callable(x) else class_decorator(x)

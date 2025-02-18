import re
import inspect
import traceback
from typing import Callable, Type, Optional, Union
from functools import wraps
from ai.src.crews.debug_crew.crew import DebugCrew


def aidebug(function: Optional[Union[Callable, Type]] = None, *, class_mode: bool = True) -> Callable:
    """Decorator that wraps test functions & test classes, invokes DebugCrew on failure, and autocorrects code.

    - Works on **functions**: `@aidebug`
    - Works on **pytest test classes**: `@aidebug(class_mode=True)`
    - Supports usage with or without parentheses: `@aidebug()` and `@aidebug`
    """

    def function_decorator(func: Callable) -> Callable:
        """Wraps individual test functions to catch exceptions and invoke DebugCrew."""

        @wraps(func)  # ✅ Keeps function signature for pytest compatibility
        def wrapper(*args: any, **kwargs: any) -> None:
            try:
                return func(*args, **kwargs)

            except Exception:
                error_trace = traceback.format_exc()
                original_code = inspect.getsource(func)

                print(f"\n❌ Test Failed: {func.__name__}\n")
                print("Traceback:\n", error_trace)
                print("\nOriginal Code:\n", original_code)

                debug_team = DebugCrew()
                fixed_code = debug_team.execute(error_trace, original_code)

                # Sanitize AI-generated code (keep this for debugging)
                cleaned_code = re.sub(r"```python\n?|```", "", fixed_code).strip()
                print("\n🔧 AI-Suggested Fix:\n", cleaned_code)

                return  # Ensure test execution stops properly on failure

        return wrapper

    def class_decorator(cls: Type) -> Type:
        """Decorator for pytest test classes (Test*), applies aidebug to all test methods but does NOT run them."""
        if not cls.__name__.startswith("Test"):  # ✅ Only wrap pytest test classes
            return cls

        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and attr_name.startswith("test"):  # ✅ Only wrap test methods
                setattr(cls, attr_name, function_decorator(attr_value))

        return cls

    # **Handle usage with or without parentheses**
    if function:
        if isinstance(function, type):  # If it's a class
            return class_decorator(function) if class_mode else function
        elif callable(function):  # If it's a function
            return function_decorator(function)

    # # If called with parentheses (@aidebug())
    return lambda x: class_decorator(x) if class_mode and isinstance(x, type) else function_decorator(x)

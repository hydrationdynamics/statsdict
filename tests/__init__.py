# -*- coding: utf-8 -*-
"""Standalone Typer app for testing statsdict."""
# standard library imports
import functools
from pathlib import Path
from typing import Callable
from typing import List

import pytest
import sh
from sh import ErrorReturnCode

STATS_PATH = Path("app_stats.json")
TESTAPP = sh.python.bake("tests/app.py")


def help_check(subcommand: str) -> str:
    """Test help function for subcommand."""
    print(f"Test {subcommand} help.")
    if subcommand == "global":
        help_command = ["--help"]
    else:
        help_command = [subcommand, "--help"]
    try:
        output = TESTAPP(help_command)
    except ErrorReturnCode as errors:
        print(errors)
        pytest.fail(f"{subcommand} help test failed")
    print(output)
    assert "Usage:" in output
    assert "Options:" in output
    return output


def print_docstring() -> Callable:
    """Decorator to print a docstring."""

    def decorator(func: Callable) -> Callable:
        """Define decorator."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Print docstring and call function."""
            print(func.__doc__)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def run_app(args: List[str]) -> str:
    """Run test app with args."""
    try:
        output = TESTAPP(args)
    except ErrorReturnCode as errors:
        print(errors)
    return output

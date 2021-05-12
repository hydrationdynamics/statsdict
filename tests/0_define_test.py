# -*- coding: utf-8 -*-
"""Tests for basic CLI function."""
import pytest
import sh

from . import help_check
from . import print_docstring
from . import STATS_PATH
from . import TESTAPP

# global constants
FIRST_RUN_TABLE = """
======  ===============  =======  =====================
Name    Value            Units    Description
======  ===============  =======  =====================
k       23
ΔH      40               kJ/mol   [activation enthalpy]
ΔS      840±3            kJ/mol   [activation entropy]
n_sigs  (2.34±0.02)×10⁴  bp       [bases in signatures]
======  ===============  =======  =====================
"""
SECOND_RUN_TABLE = """
======  ===============  =======  =====================
Name    Value            Units    Description
======  ===============  =======  =====================
k       23
n_sigs  (2.34±0.02)×10⁴  bp       [bases in signatures]
======  ===============  =======  =====================
"""


def test_global_help():
    """Test global help function."""
    output = help_check("global")
    found_commands = False
    commands = []
    for line in output:
        if not found_commands:
            if line.startswith("Commands"):
                found_commands = True
                continue
        else:
            commands.append(line.strip().split()[0])
    assert "define" in commands
    assert "stats" in commands


@print_docstring()
def test_cleanup() -> None:
    """Clean up test directory."""
    if STATS_PATH.exists():
        STATS_PATH.unlink()


@print_docstring()
def test_first_define():
    """Test first stat definitions."""
    try:
        output = TESTAPP(["define"])
    except sh.ErrorReturnCode as errors:
        print(errors)
        pytest.fail(errors)
    assert FIRST_RUN_TABLE in output


@print_docstring()
def test_second_define():
    """Test second stat definitions."""
    try:
        output = TESTAPP(["define"])
    except sh.ErrorReturnCode as errors:
        print(errors)
        pytest.fail(errors)
    assert SECOND_RUN_TABLE in output

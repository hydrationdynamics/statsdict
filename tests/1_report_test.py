# -*- coding: utf-8 -*-
"""Tests for basic CLI function."""
# third-party imports
import pytest
import sh

from . import print_docstring
from . import TESTAPP

# global constants
ALL_RUNS_TABLE = """
======  ===============  =======  =====================  =====
Name    Value            Units    Description              Run
======  ===============  =======  =====================  =====
k       23                                                   2
ΔH      40               kJ/mol   [activation enthalpy]      1
ΔS      840±3            kJ/mol   [activation entropy]       1
n_sigs  (2.34±0.02)×10⁴  bp       [bases in signatures]      2
======  ===============  =======  =====================  =====
"""
SINGLE_STAT = "n_sigs"
SINGLE_STAT_REPORT = "(2.34±0.02)×10⁴ bp"


@print_docstring()
def test_all_stats_report():
    """Test reporting all stats."""
    try:
        output = TESTAPP(["stats"])
    except sh.ErrorReturnCode as errors:
        print(errors)
        pytest.fail(errors)
    assert ALL_RUNS_TABLE in output


@print_docstring()
def test_single_stat_report():
    """Test reporting a single stat."""
    try:
        output = TESTAPP(["stats", "--name", SINGLE_STAT])
    except sh.ErrorReturnCode as errors:
        print(errors)
        pytest.fail(errors)
    assert output.strip() == SINGLE_STAT_REPORT

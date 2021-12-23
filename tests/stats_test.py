# -*- coding: utf-8 -*-
"""Tests for basic CLI function."""
# third-party imports
from statsdict import Stat
from statsdict import StatsDict

from . import print_docstring
from . import working_directory


@print_docstring()
def test_stats(tmp_path):
    """Test stats functionality."""
    with working_directory(tmp_path):
        new_units = [
            "basepairs = [dimensionless] = bp",
            "kilobasepairs = 1000 * basepairs = kbp",
        ]
        stats = StatsDict()

        @stats.auto_save_and_report
        def define_some_stats() -> None:
            """Stat definitions in a function."""
            run_no = stats.run_no
            stats.define_units(new_units)
            stats["k"] = Stat(23)
            if run_no % 2:
                stats["ΔH"] = Stat(
                    40.0, units="kJ/mol", desc="activation enthalpy"
                )
                stats["ΔS"] = Stat(
                    840.0,
                    uncert=3.1,
                    units="kJ/mol",
                    desc="activation entropy",
                )
            if run_no % 3:
                stats["n_sigs"] = Stat(
                    23400,
                    units="basepairs",
                    is_count=True,
                    desc="bases in signatures",
                )
            print(stats)

        define_some_stats()

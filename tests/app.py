"""Simple Typer app for testing."""
from __future__ import annotations

import sys

import loguru
import typer
from loguru import logger
from statsdict import Stat
from statsdict import StatsDict

# global constants
DEFAULT_STDERR_LOG_LEVEL = "INFO"
NO_LEVEL_BELOW = 30  # Don't print level for messages below this level
NAME = "app"
VERSION = "0.0.1"


def _stderr_format_func(record: loguru.Record) -> str:
    """Do level-sensitive formatting."""
    if record["level"].no < NO_LEVEL_BELOW:
        return "<level>{message}</level>\n"
    return "<level>{level}</level>: <level>{message}</level>\n"


# set up logging
logger.remove()
logger.add(
    sys.stderr, level=DEFAULT_STDERR_LOG_LEVEL, format=_stderr_format_func
)
# instantiate app and stats
app = typer.Typer(help=__doc__, name=NAME)
stats = StatsDict(module_name=NAME, logger=logger, verbose=True, app=app)


@app.command()
@stats.auto_save_and_report
def define() -> None:
    """Stat definitions in a function."""
    run_no = stats.run_no
    new_units = [
        "basepairs = [dimensionless] = bp",
        "kilobasepairs = 1000 * basepairs = kbp",
    ]
    stats.define_units(new_units)
    stats["k"] = Stat(23)
    if run_no % 2:
        stats["ΔH"] = Stat(40.0, units="kJ/mol", desc="activation enthalpy")
        stats["ΔS"] = Stat(
            840.0, uncert=3.1, units="kJ/mol", desc="activation entropy"
        )
    if run_no % 3:
        stats["n_sigs"] = Stat(
            23400,
            units="basepairs",
            is_count=True,
            desc="bases in signatures",
        )
    logger.info("Test done")


def main() -> None:
    """Run the app."""
    app()


if __name__ == "__main__":
    main()

"""
Main entry point.
"""

# pylint: disable=all
# flake8: noqa

import argparse
from create_python_cmd.createapp import create_python_app


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    parser = argparse.ArgumentParser(prog="createpythonapp")
    args = parser.parse_args()
    create_python_app()
    return 0

#!/usr/bin/env python3

# Packages
from setuptools import setup, find_packages

with open("sensors/__init__.py") as f:
    info = {}
    for line in f:
        if line.startswith("__version__"):
            exec(line, info)
            break

# Setup
setup(
        name = "R-OSE",
        version = info["__version__"],
        author = "William L. Fauteux",
        description = "Reusable Open Stratospheric Explorer (R-OSE) - Flight data logging program",
        long_description = "This program is used aboard the platform to gather information regarding flight conditions.",
        packages = find_packages(),
        install_requires = [
            "smbus",
            "numpy"
            ]
        )


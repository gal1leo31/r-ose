#!/usr/bin/env python3

# Packages
from setuptools import setup, find_packages

from sensors import __version__

# Setup
setup(
        name = "R-OSE",
        fullname = "Reusable Open Stratospheric Explorer",
        version = __version__,
        author = "William L. Fauteux",
        packages = find_packages(),
        install_requires = [
            "smbus",
            "numpy"
            ]
        )


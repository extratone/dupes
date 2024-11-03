# setup.py

import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import sys

class CustomInstallCommand(install):
    """Custom installation to handle man page installation."""

    def run(self):
        super().run()
        man_page_source = "dupes.1"
        man_page_dest = "/usr/local/share/man/man1/dupes.1"  # Default for Unix-like systems

        if sys.platform == "darwin":  # macOS
            man_page_dest = "/usr/local/share/man/man1/dupes.1"
        elif sys.platform.startswith("linux"):
            man_page_dest = "/usr/share/man/man1/dupes.1"

        os.makedirs(os.path.dirname(man_page_dest), exist_ok=True)
        self.copy_file(man_page_source, man_page_dest)
        print(f"Installed man page to {man_page_dest}")

setup(
    name="dupes-cli",  # Renamed package name for PyPI
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dupes=dupes.main:main",  # Command-line entry point remains "dupes"
        ],
    },
    install_requires=[],
    description="A CLI tool to find and manage duplicate files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="David Blue",
    author_email="davidblue@extratone.com",
    url="https://github.com/extratone/dupes",  # Update this with the real URL for dupes-cli
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    data_files=[("", ["dupes.1"])],
    cmdclass={
        "install": CustomInstallCommand,
    },
)

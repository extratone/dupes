from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dupes",
    version="0.1.0",  # Update with your version
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line tool to find and delete duplicate files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dupes = dupes:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    data_files=[
        ("man/man1", ["dupes.1"])
    ],
)

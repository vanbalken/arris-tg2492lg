import re

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Read the version without importing the package, which needs aiohttp.
with open("arris_tg2492lg/const.py", "r") as fh:
    version = re.search(r'^__version__ = "([^"]+)"', fh.read(), re.MULTILINE).group(1)

setup(
    name="arris-tg2492lg",
    version=version,
    author="vanbalken",
    description="Python client for the Arris TG2492LG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanbalken/arris-tg2492lg",
    packages=find_packages(exclude=['tests']),
    install_requires=["aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

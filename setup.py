from setuptools import find_packages, setup
import arris_tg2492lg.const as arris_const

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="arris-tg2492lg",
    version=arris_const.__version__,
    author="vanbalken",
    description="Python client for the Arris TG2492LG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanbalken/arris-tg2492lg",
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

from setuptools import setup, find_packages
import os

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pystibmivb",
    version="0.2.4.2",
    author="Daniel Nix",
    author_email="daniel.nix@gmail.com",
    description="A Python wrapper for the Stib-Mivb API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danito/pyStibMivb",
    install_requires=['requests>=2.0','xmltodict>=0.11.0'],
    python_requires='>=3',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

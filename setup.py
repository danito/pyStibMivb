from setuptools import setup, find_packages
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pystibmivb",
    version=version,
    author="Daniel Nix",
    author_email="me@nixis.me",
    description="A Python wrapper for the Stib-Mivb API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danito/pyStibMivb",
    install_requires=['requests>=2.0'],
    python_requires='>=3',
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ),
)

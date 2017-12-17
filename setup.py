from setuptools import setup, find_packages

from asyncserver import __version__

setup(
    name="django-asyncserver",
    version=__version__,
    packages=find_packages(),
)

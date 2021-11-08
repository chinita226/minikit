"""Root."""
from setuptools import setup, find_packages

setup(
    test_suite='tests',
    name='app',
    version='0.2.0',
    packages=find_packages(include=['app', 'app.*'])
)

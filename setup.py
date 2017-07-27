import re

from setuptools import setup, find_packages

with open('src/autovalue.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
    assert version is not None

setup(name='AutoValue',
      version=version,
      author='Jean Giard',
      license='LGPL',
      classifier=[
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(where='src'),
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      )

import re

from setuptools import setup

with open('autovalue/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
    assert version is not None

setup(name='AutoValue',
      version=version,
      author='Jean Giard',
      license='LGPL',
      packages=['autovalue'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      )

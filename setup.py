from setuptools import setup, find_packages
from setuptools.command.install import install

setup(name="count_sum",
      version="1.0.0",
      description="Sums and filters count files",
      license="MIT",
      author="William Patterson",
      packages=find_packages(),
      entry_points={"console_scripts": ["csum=count_sum.__main__:main"],})

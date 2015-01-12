from setuptools import setup, find_packages

setup(
    name="saio-fuse",
    version="0.1",
    description="fill me out",
    author='Richard Hawkins',
    url='https://github.com/hurricanerix/saio-fuse.git',
    packages=find_packages().append('fusepy'),
)

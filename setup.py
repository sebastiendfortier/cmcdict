from setuptools import setup, find_packages

with open('VERSION', encoding='utf-8') as f:
    version = f.read()
release = version

setup(
    name='cmcdict',
    version=release,
    description='python library to work with cmc operation dictionnary',
    author='Sebastien Fortier',
    author_email='sebastien.fortier@ec.gc.ca',
    packages=find_packages(),
    package_data = {
    'cmcdict': ['VERSION'],
  }
)

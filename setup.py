"""setup.py module installer"""
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

with open('VERSION') as f:
    VERSION = f.read()

REQUIRED = ['pycrypto']

setup(
    name='zcu',
    version=VERSION,
    description='ZTE Configuration Utility',
    long_description=README,
    author='Mark Street',
    author_email='mkst@protonmail.com',
    url='https://github.com/streetster/zte-config-utility',
    license=LICENSE,
    install_requires=REQUIRED,
    packages=find_packages(exclude=('tests', 'docs'))
)

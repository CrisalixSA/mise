import os
from setuptools import setup, find_packages
from distutils.extension import Extension
from pkg_resources import parse_requirements
from Cython.Build import cythonize


PACKAGE_NAME = 'mise'
VERSION = '0.1'
REQUIREMENTS_FILE_PATH = 'requirements.txt'

# Gather all extension modules
ext_modules = [
    Extension(
        'mise',
        sources=[
            'lib/mise.pyx'
        ],
    )
]

# Build setup
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    install_requires=[
        req.__str__()
        for req in parse_requirements(open(REQUIREMENTS_FILE_PATH).read())
    ],
    ext_modules=cythonize(ext_modules),
)

import io
import os
import re
from codecs import open     # To use consistent encodings
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize


PACKAGE_NAME = 'mise'
PACKAGE_PATH = 'lib'
VERSION_FILE_PATH = os.path.join(PACKAGE_PATH, '__init__.py')
REQUIREMENTS_FILE_PATH = 'requirements.txt'


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version(VERSION_FILE_PATH)

with open(REQUIREMENTS_FILE_PATH, 'r') as requirements_file:
    text = requirements_file.read()
requirements_text = re.sub(r'^\s*\-e\s+([^=]+)=([^\n]+)', r'\2 @ \1=\2', text, flags=re.MULTILINE)

setup(
    name=PACKAGE_NAME,
    version=__version__,
    ext_modules=cythonize([
        Extension(
            PACKAGE_NAME,
            sources=[
                f'{PACKAGE_PATH}/mise.pyx',
            ],
        ),
    ])
)

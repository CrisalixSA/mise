import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize

PACKAGE_NAME = 'mise'
PACKAGE_PATH = PACKAGE_NAME
VERSION_FILE_PATH = os.path.join(PACKAGE_PATH, '__init__.py')
REQUIREMENTS_FILE_PATH = 'requirements.txt'
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Extensions
# mise (efficient mesh extraction)
mise_module = Extension(
    'mise',
    sources=[
        'lib/mise.pyx'
    ],
)

# Gather all extension modules
ext_modules = [
    mise_module
]

setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    ext_modules=cythonize(ext_modules),
    author='Crisalix SA',
    description='Python package for MISE surface extraction',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    project_urls={
        'Bug Tracker': 'https://github.com/CrisalixSA/h3ds/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={PACKAGE_NAME: PACKAGE_PATH},
    packages=find_packages(
        include=[PACKAGE_NAME],
        exclude=[],
    ),
    install_requires=[
        'numpy~=1.16.4'
    ]
)
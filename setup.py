try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

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
    name='mise',
    version='0.1',
    ext_modules=cythonize(ext_modules)
)
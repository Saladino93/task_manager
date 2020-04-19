from distutils.core import setup, Extension
import os

setup(name='taskmanager',
      version='0.1',
      description='Pipeline manager.',
      url='https://github.com/Saladino93/',
      author='Omar Darwish',
      author_email='od261@cam.ac.uk',
      license='BSD-2-Clause',
      packages=['taskmanager'],
      package_dir={'taskmanager':'taskmanager'},
      zip_safe=False)

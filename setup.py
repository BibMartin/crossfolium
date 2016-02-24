# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

rootpath = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.verbose = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


def extract_version(module='crossfolium'):
    version = None
    fname = os.path.join(rootpath, module, '__init__.py')
    with open(fname) as f:
        for line in f:
            if (line.startswith('__version__')):
                _, version = line.split('=')
                version = version.strip()[1:-1]  # Remove quotation characters.
                break
    return version

pkg_data = {'': []}
pkgs = [
    'crossfolium',
    ]

LICENSE = read('LICENSE.txt')
long_description = '{}\n{}'.format(read('README.md'), read('CHANGES.txt'))

# Dependencies.
with open('requirements.txt') as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]


config = dict(name='crossfolium',
              version=extract_version(),
              description='Add crossfilters in folium',
              long_description=long_description,
              author='Martin Journois',
              url='https://github.com/bibmartin/crossfolium',
              keywords='folium crossfilter data visualization',
              classifiers=['Programming Language :: Python :: 2.7',
                           'Programming Language :: Python :: 3.4',
                           'Programming Language :: Python :: 3.5',
                           'License :: OSI Approved :: MIT License',
                           'Development Status :: 5 - Production/Stable'],
              packages=pkgs,
              package_data=pkg_data,
              cmdclass=dict(test=PyTest),
              tests_require=['pytest'],
              license=LICENSE,
              install_requires=install_requires,
              zip_safe=False)


setup(**config)

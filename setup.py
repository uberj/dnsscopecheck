#!/usr/bin/env python

from distutils.core import setup

setup(name='dnsscopecheck',
    version='1.0',
    description='Finds errors in DNS zone files',
    author='Jacques Uber',
    author_email='juber@mozilla.com',
    packages=['dnsscopecheck'],
    package_data={
        'dnsscopecheck': ['dnsscopecheck/check.py', 'dnsscopecheck/paths.py'],
    },
    scripts=['bin/dnsscopecheck'],
    url='https://github.com/uberj/dnsscopecheck',
    license='LICENSE.txt',
)

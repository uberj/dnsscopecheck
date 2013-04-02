#!/usr/bin/env python

from distutils.core import setup

setup(name='fixdns',
    version='1.0',
    description='Finds errors in DNS zone files',
    author='Jacques Uber',
    author_email='juber@mozilla.com',
    packages=['fixdns'],
    package_data={
        'fixdns': ['fixdns/fix.py', 'fixdns/paths.py'],
    },
    scripts=['bin/fixdns'],
    url='https://github.com/uberj/fixdns',
    license='LICENSE.txt',
)

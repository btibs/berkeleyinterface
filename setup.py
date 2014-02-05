#!/usr/bin/env python
# setup
# Setup script for BerkeleyInterface
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Feb 05 09:07:42 2014 -0500
#
# Copyright (C) 2013 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: setup.py [] bengfort@cs.umd.edu $

"""
Setup script for BerkeleyInterface
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

packages = find_packages(where=".", exclude=("tests", "bin", "docs", "fixtures",))
requires = []

with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        if line.startswith('#'): continue
        requires.append(line.strip())

classifiers = (
    'Development Status :: 3 - Alpha',
    'Environment :: MacOS X',
    'Environment :: Console',
    'Environment :: Other Environment',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Java',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries :: Java Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
)

config = {
    "name": "BerkeleyInterface",
    "version": "0.2",
    "description": "A Python wrapper for the Berkeley Parser",
    "author": "Elizabeth McNany",
    "author_email": "beth@cs.umd.edu",
    "url": "https://github.com/mclumd/berkeleyinterface",
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "zip_safe": True,
    "scripts": [],
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)

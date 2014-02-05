# tests
# Testing for the Berkeley Interface Package
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Feb 05 09:05:45 2014 -0500
#
# Copyright (C) 2013 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
Testing for the Berkeley Interface Package
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest

##########################################################################
## TestCases
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test a simple world fact to kick off testing
        """
        self.assertEqual(2**3, 8)

    @unittest.skip("Need to find way to install JPype on Travis")
    def test_import(self):
        """
        We are able to import our packages
        """
        try:
            import BerkeleyInterface as berkeley
        except ImportError:
            self.fail("Unable to import the BerkeleyInterface module!")

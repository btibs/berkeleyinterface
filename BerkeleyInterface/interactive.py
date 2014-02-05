# BerkeleyInterface.interactive
# An interactive console to the Berkeley Parser
#
# Author:   Elizabeth McNany <beth@cs.umd.edu>
# Created:  Tue Jul 16 16:40:22 2013 -0400
#
# Copyright (C) 2013 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: interactive.py [] beth@cs.umd.edu $

"""
Basic example demonstrating usage of the interface: Interactive console version!
User can enter utterances repeatedly and exit with ctrl-c
"""

##########################################################################
## Imports
##########################################################################

from berkeleyinterface import *
from StringIO import StringIO
import sys

##########################################################################
## Main functionality
##########################################################################

# Allow entering a number for kbest parses to show when running
kbest = 1
if len(sys.argv) > 1:
    kbest = int(sys.argv[1])

# This should be the path to the Berkeley Parser jar file
cp = r'C:\berkeleyparser\BerkeleyParser-1.7.jar'

# Always start the JVM first!
startup(cp)

# Set input arguments
# See the BerkeleyParser documentation for information on arguments
gr = r'C:\berkeleyparser\eng_sm6.gr'
args = {"gr":gr, "tokenize":True, "kbest":kbest}

# Convert args from a dict to the appropriate Java class
opts = getOpts(dictToArgs(args))

# Load the grammar file and initialize the parser with our options
parser = loadGrammar(opts)

# Now, run the parser
print "Enter your input below:\n"
while True:
    try:
        # User can type into the console and the parse will be written to stdout
        strIn = StringIO(raw_input(" > ")) # yes, this is still 2.7...
        strOut = StringIO()
        parseInput(parser, opts, inputFile=strIn, outputFile=strOut)
        print strOut.getvalue()
    except EOFError:
        print "\n\nGoodbye."
        break

# That's all, folks!
shutdown()

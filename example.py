'''
Basic example demonstrating usage of the interface
'''

from berkeleyinterface import *

# This should be the path to the Berkeley Parser jar file
cp = r'C:\berkeleyparser\BerkeleyParser-1.7.jar'

# Always start the JVM first!
startup(cp)

# Set input arguments
# See the BerkeleyParser documentation for information on arguments
# Notably: a grammar file ("gr") is required, and if inputFile / outputFile
# are not given, it will default to stdin/stdout
gr = r'C:\berkeleyparser\eng_sm6.gr'
args = {"gr":gr, "tokenize":True, "inputFile":"testinput.txt"}

# Convert args from a dict to the appropriate Java class
opts = getOpts(dictToArgs(args))

# Load the grammar file and initialize the parser with our options
parser = loadGrammar(opts)

# Now, actually parse the input file
# (Since we didn't specify an output file, it will go to stdout)
parseInput(parser, opts)

# At this point, we have done the equivalent of running from the command line:
# java -client -jar C:\berkeleyparser\BerkeleyParser-1.7.jar\BerkeleyParser-1.7.jar -gr eng_sm6.gr -inputFile testinput.txt -tokenize

# We can change opts between parses, in this case to change input/outputs
# See documentation for getOpts for a list of options which are safe to modify
# and will not require reinitializing the parser
opts.inputFile = "testinput2.txt"
opts.outputFile = opts.inputFile + ".parsed"

# Or, we could modify the original args dictionary:
args["inputFile"] = "testinput2.txt"
args["outputFile"] = args["inputFile"] + ".parsed"
opts = getOpts(dictToArgs(args))

# Parse again, with our modified options
parseInput(parser, opts)

# That's all, folks!
shutdown()
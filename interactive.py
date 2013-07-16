'''
Basic example demonstrating usage of the interface: Interactive console version!
'''

from berkeleyinterface import *

# This should be the path to the Berkeley Parser jar file
cp = r'C:\berkeleyparser\BerkeleyParser-1.7.jar'

# Always start the JVM first!
startup(cp)

# Set input arguments
# See the BerkeleyParser documentation for information on arguments
gr = r'C:\berkeleyparser\eng_sm6.gr'
args = {"gr":gr, "tokenize":True}

# Convert args from a dict to the appropriate Java class
opts = getOpts(dictToArgs(args))

# Load the grammar file and initialize the parser with our options
parser = loadGrammar(opts)

# Now, run the parser
print "Enter your input below:\n"
try:
    # User can type into the console and the parse will be written to stdout
    parseInput(parser, opts)
except: # this doesn't actually work, ctrl-c still just quits immediately
    print "Caught error: ",sys.exc_info()
    
# That's all, folks!
shutdown()

'''
Python interface to the Berkeley Parser

This has the advantage over other implementations which essentially automate a
call to the jar file: this actually duplicates the main() method, allowing
multiple parse calls and ability to modify options without the overhead of
loading the grammar file each time (and without having to use Java!)
'''

import sys
import re
import jpype
from StringIO import StringIO

def __outputTrees(parseTrees, outputData, parser, opts, line, sentenceID):
    '''
    Write tree information to outputData. This is a reimplementation of the
    private method of the same name from BerkeleyParser.java.
    '''
    # todo cleanup?
    delimiter = "\t"
    if opts.ec_format:
        newList = []
        for parsedTree in parseTrees:
            if parsedTree.getChildren().isEmpty():
                continue
            if parser.getLogLikelihood(parsedTree) != float("-inf"):
                newList.append(parsedTree)
        parseTrees = newList
        outputData.write("%s\t%s\n" % (len(parseTrees), sentenceID))
        delimiter = ",\t"
    
    for parsedTree in parseTrees:
        addDelimiter = False
        if opts.tree_likelihood:
            treeLL = float("-inf") if parsedTree.getChildren().isEmpty() \
                else parser.getLogLikelihood(parsedTree)
            if treeLL == float("-inf"):
                continue
            outputData.write("%s"%treeLL)
            addDelimiter = True
        if opts.sentence_likelihood:
            allLL = float("-inf") if parsedTree.getChildren().isEmpty() \
                else parser.getLogLikelihood()
            if addDelimiter:
                outputData.write(delimiter)
            addDelimiter = True
            if opts.ec_format:
                outputData.write("sentenceLikelihood ")
            outputData.write("%s"%allLL)
        if not opts.binarize:
            TreeAnnotations = jpype.JClass("edu.berkeley.nlp.PCFGLA.TreeAnnotations")
            parsedTree = TreeAnnotations.unAnnotateTree(parsedTree, opts.keepFunctionLabels)
        if opts.confidence:
            treeLL = float("-inf") if parsedTree.getChildren().isEmpty() \
                else parser.getConfidence(parsedTree)
            if addDelimiter:
                outputData.write(delimiter)
            addDelimiter = True
            if opts.ec_format:
                outputData.write("confidence ")
            outputData.write("%s"%treeLL)
        elif opts.modelScore:
            score = float("-inf") if parsedTree.getChildren().isEmpty() \
                else parser.getModelScore(parsedTree)
            if addDelimiter:
                outputData.write(delimiter)
            addDelimiter = True
            if opts.ec_format:
                outputData.write("maxRuleScore ")
            outputData.write("%.8f"%score)
        
        if opts.ec_format:
            outputData.write("\n")
        elif addDelimiter:
            outputData.write(delimiter)
        if not parsedTree.getChildren().isEmpty():
            treeString = parsedTree.getChildren().get(0).toString()
            if len(parsedTree.getChildren()) != 1:
                sys.stderr.write("ROOT has more than one child!")
                parsedTree.setLabel("")
                treeString = parsedTree.toString()
            if opts.ec_format:
                outputData.write("(S1 " + treeString + " )\n");
            else:
                outputData.write("( " + treeString + " )\n");
        else:
            outputData.write("(())\n")
        if opts.render:
            try:
                writeTreeToImage(parsedTree, re.sub("[^a-zA-Z]", "", line) + ".png")
            except jpype.JException(java.lang.RuntimeException), ex:
                #todo actually test this exception handling
                print "Caught the runtime exception : ", JavaException.message()
                print JavaException.stackTrace()
    if opts.dumpPosteriors:
        blockSize = 50
        fileName = opts.grFileName + ".posteriors"
        parser.dumpPosteriors(fileName, blockSize)
    
    if opts.kbest > 1:
        outputData.write("\n")
    
    outputData.flush()

def startup(classpath):
    '''Start the JVM. This MUST be called before any other jpype functions!'''
    # regarding memory - YMMV; this worked for my setup
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % classpath, "-Xmx500m")

def dictToArgs(d):
    '''Convert a dict of options to a list of command-line-style args'''
    boolDefaults = [ "tokenize", "binarize", "scores", "keepFunctionLabels",
        "substates", "accurate", "modelScore", "confidence", "sentence_likelihood",
        "tree_likelihood", "variational", "render", "chinese", "useGoldPOS",
        "dumpPosteriors", "ec_format",
    ] # these all default to False and only require the switch if True
    
    # get a list of "-key", "value" or just "-key" if key is in boolDefaults
    args = [j for i in [("-"+k, '%s'%v) if k not in boolDefaults else ("-"+k,) for k,v in d.iteritems()] for j in i]
    return args
    
def getOpts(args):
    '''
    Converts given command-line-style args to opts for parser functions.
    
    Note that changing options for:
        accurate, chinese, grFileName, kbest, nGrammars, nThreads, scores,
        substates, viterbi, variational
    after calling loadGrammar will NOT update the parser.
    
    Specifically, options for:
        grFileName, kbest, nThreads
    are used in both parser setup (loadGrammar) and actual parsing (parseInput)
    
    Options for:
        binarize, confidence, dumpPosteriors, ec_format, goldPOS, inputFile,
        keepFunctionLabels, maxLength, modelScore, outputFile, render,
        sentence_likelihood, tokenize, tree_likelihood
    do not affect the grammar loading and may be changed between those steps.
    
    The JVM must be started before calling this function.
    '''
    Options = jpype.JClass("edu.berkeley.nlp.PCFGLA.BerkeleyParser$Options")
    OptionParser = jpype.JClass("edu.berkeley.nlp.PCFGLA.OptionParser")
    optParser = OptionParser(Options)
    opts = optParser.parse(args, True)
    return opts
    
def loadGrammar(opts):
    '''
    Loads the grammar and lexicon for the parser, given options.
    Returns the initialized parser.
    '''
    threshold = 1.0

    if opts.chinese: #todo WARNING: THIS IS UNTESTED
        Corpus = jpype.JClass("edu.berkeley.nlp.PCFGLA.Corpus")
        Corpus.myTreebank = Corpus.TreeBankType.CHINESE

    parser = None
    
    # load grammar
    if opts.nGrammars != 1: #todo
        print "Multiple grammars not implemented!"
        sys.exit(1)
    else:
        inFileName = opts.grFileName
        ParserData = jpype.JClass("edu.berkeley.nlp.PCFGLA.ParserData")
        pData = ParserData.Load(inFileName)
        if pData is None:
            print "Failed to load grammar from file '%s'."%inFileName
            sys.exit(1)
        grammar = pData.getGrammar()
        lexicon = pData.getLexicon()
        Numberer = jpype.JClass("edu.berkeley.nlp.util.Numberer")
        Numberer.setNumberers(pData.getNumbs())
        if opts.kbest == 1:
            CoarseToFineMaxRuleParser = jpype.JClass("edu.berkeley.nlp.PCFGLA.CoarseToFineMaxRuleParser")
            parser = CoarseToFineMaxRuleParser(grammar, lexicon, threshold, -1,
                opts.viterbi, opts.substates, opts.scores, opts.accurate, opts.variational,
                True, True)
        else:
            CoarseToFineNBestParser = jpype.JClass("edu.berkeley.nlp.PCFGLA.CoarseToFineNBestParser")
            parser = CoarseToFineNBestParser(grammar, lexicon, opts.kbest, threshold,
                -1, opts.viterbi, opts.substates, opts.scores, opts.accurate,
                opts.variational, False, True)
        
        parser.binarization = pData.getBinarization()
        #end else (if nGrammars != 1)
    
    if opts.nThreads > 1:#todo
        m_parser = None
        print "Multiple threads not implemented!"
        sys.exit(-1)
    
    return parser
    # end loadGrammar
    
def parseInput(parser, opts, inputFile=None, outputFile=None):
    '''
    Uses parser with opts to parse the input file to output file.
    Optional arguments inputFile and outputFile overwrite values in opts.
    If a StringIO object is used as output, it will not be closed.
    '''
    # initialize input/outputs
    inputData = sys.stdin
    if inputFile:
        if isinstance(inputFile, StringIO):
            inputData = inputFile
        else:
            inputData = file(inputFile, 'r')
    elif opts.inputFile:
        inputData = file(opts.inputFile, 'r')
    
    outputData = sys.stdout
    if outputFile:
        if isinstance(outputFile, StringIO):
            outputData = outputFile
        else:
            outputData = file(outputFile, 'w')
    elif opts.outputFile:
        outputData = file(opts.outputFile, 'w') 
    
    # read in data
    sentenceID = ""
    line = inputData.readline()
    while line != '':
        line = line.strip()
        if opts.ec_format and line == "":
            continue
        
        sentence = None
        posTags = None
        
        if opts.goldPOS: # format: "word\tPOS-...\n"; newline between sentences
            sentence = []
            posTags = []
            tmp = line.split("\t")
            if len(tmp) == 0:
                continue
            sentence.append(tmp[0])
            tags = tmp[1].split("-")
            posTags.append(tags[0])
            
            line = inputData.readline().strip() # need to remove newlines
            while line != '':
                tmp = line.split("\t")
                if len(tmp) == 0:
                    break
                sentence.append(tmp[0])
                tags = tmp[1].split("-")
                posTags.append(tags[0])
                line = inputData.readline().strip()
        else:
            if opts.ec_format:
                breakIndex = line.index(">")
                sentenceID = line[3:breakIndex-1]
                line = line[breakIndex+2:len(line)-5]
            if not opts.tokenize:
                sentence = re.split(r'\s+', line)
            else:
                PTBLineLexer = jpype.JClass("edu.berkeley.nlp.io.PTBLineLexer")
                tokenizer = PTBLineLexer()
                sentence = tokenizer.tokenizeLine(line)
        
        if len(sentence) > opts.maxLength:
            outputData.write("(())\n");
            sys.stderr.write("Skipping sentence with %s words since it is too long.")
            continue
        
        if opts.nThreads > 1: #todo
            print "Multiple threads still not implemented!"
            sys.exit(-1)
        else:
            parsedTrees = []
            if opts.kbest > 1:
                parsedTrees = parser.getKBestConstrainedParses(sentence, posTags, opts.kbest)
                if len(parsedTrees) == 0:
                    Tree = jpype.JClass("edu.berkeley.nlp.syntax.Tree")
                    parsedTrees.append(Tree("ROOT"))
            else:
                parsedTrees = []
                pt = None
                if posTags != None:
                    pt = jpype.java.util.ArrayList()
                    for p in posTags:
                        pt.add(p)
                st = jpype.java.util.ArrayList()
                for s in sentence:
                    st.add(s)
                # postags will be None unless using option goldPOS
                # len(posTags) == len(sentence)
                parsedTree = parser.getBestConstrainedParse(st, pt, None)
                if opts.goldPOS and parsedTree.getChildren().isEmpty():
                    # comment in Java: "parse error when using goldPOS, try without"
                    # This will ignore any given tags and just use the default tagger
                    parsedTree = parser.getBestConstrainedParse(sentence, None, None)
                parsedTrees.append(parsedTree)
        
            # using the reimplemented function because the Java method is private
            __outputTrees(parsedTrees, outputData, parser, opts, line, sentenceID)
        
        line = inputData.readline()
        # end while
    
    if opts.nThreads > 1: #todo
        print "Multiple threads still definitely not implemented!"
        sys.exit(-1)
    
    if opts.dumpPosteriors:
        fileName = opts.grFileName + ".posteriors"
        parser.dumpPosteriors(fileName, -1)
    
    '''close files'''
    inputData.close()
    outputData.flush()
    if outputData != sys.stdout and not isinstance(outputData, StringIO):
        outputData.close()
    #end parseInput

def shutdown():
    '''Shut down the JVM'''
    jpype.shutdownJVM()

# todo command-line usage w/argparse?

Python interface to the Berkeley Parser
---------------------------------------

This has the advantage over other implementations which essentially automate a call to the jar file: this actually duplicates the main() method, allowing multiple parse calls and ability to modify options without the overhead of loading the grammar file each time (and without having to use Java!)

N.B. several features completely ignored (notably, -nThreads, -nGrammars, -kbest options) and some untested (-chinese)

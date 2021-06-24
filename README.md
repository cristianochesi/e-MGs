# PMG
Phase-based Minimalist Grammars (v 0.1)
===================================================

This is a simple Python3 implementation of the Phase-based Minimalist Grammar (PMG) as discussed in Chesi 2021.
Merge is extectation-based, that is, each categorory (X) must be selected by a superordinate note (=X).
Items with unexpected unlicensed categories are moved in the Memory-buffer of the superordinate node and trasmitted to sequential phases (last-selected categories).
Items selected while the superordinate node has other selection features are "nested phases" and cannot receive any pending item (unless they become sequential at some point of the derivation and "late expansion" of selectin is permitted by parsing parameterization)

Background
----------

Phase-based MGs are an extention of MGs as proposed by Stabler (1997) and variously re-defined in various works. Notably:

- Bianchi Valentina, Cristiano Chesi (2006): [Phases, Left Branch Islands, and Computational Nesting](https://repository.upenn.edu/pwpl/vol12/iss1/3/)
- Chesi Cristiano (2019): [An efficient Trie for binding (and movement)](http://ceur-ws.org/Vol-2253/paper07.pdf)
- Chesi Cristiano, Pauli Brattico (2018): [Larger than expected: constraints on pied-piping across languages](https://lingbuzz.com/j/rgg/2018/2018.04/chesi+brattico_constraints-on-pied-piping-across-languages_RGG-2018-04.pdf)
- Chesi Cristiano, Paolo Canal (2019): [Person Features and Lexical Restrictions in Italian Clefts](https://www.frontiersin.org/articles/10.3389/fpsyg.2019.02105/full)
- De Santo, Aniello (2019): [Testing a Minimalist Grammar Parser on Italian Relative Clause Asymmetries](https://www.aclweb.org/anthology/W19-2911.pdf)
- Gerth, Sabrina: [Memory Limitations in Sentence Comprehension](https://publishup.uni-potsdam.de/opus4-ubp/frontdoor/index/index/docId/7155)
- Graf, Thomas, James Monette, and Chong Zhang (2017): [Relative Clauses as a Benchmark for Minimalist Parsing](https://thomasgraf.net/doc/papers/GrafEtAl17JLM.pdf)
- Kobele Gregory M., Sabrina Gerth, John Hale (2013): Memory Resource Allocation in Top-Down Minimalist Parsing
- Stabler, Edward (1997): [Derivational Minimalism](http://www.linguistics.ucla.edu/people/stabler/eps-lacl.pdf)
- Stabler, Edward (2013): [Two Models of Minimalist, Incremental Syntactic Analysis](http://www.linguistics.ucla.edu/people/stabler/Stabler12-2models.pdf)

Quick Start Guide
-----------------
`MG_start.py` is ready to process canonical complex sentences in Italian. A simple lexicon is provided in json format to test the capabilities of the grammar.
Also a parameterization file (json format) is provided, specifying mandatory agreement categories in Italian and English (unification algorithm to be implemented) 

`MG_grammar.py` implements the basic Merge, Move and Agree structure building operations.

`MG_parser.py` implements the basic Top-Down parsing algoritm (lexical ambiguity resolution still to be implemented)

`MG_generator.py` implements the basic Top-Down generation algorithm; this is an interactive procedure that ask you to pick up a ROOT node then feed the structure with your input

`MG_tree.py` implements an useful funzion print_node(MG_done) that print the tree in LATEX-FOREST format as in Kobele et al. 2013, Graf et al. 2017

`MG_xx.py` provide other utilities to deal with Nodes and Trees - some fixes needed

Complexity Metrics
------------------
Basic complexity Metrics inspired by Graf et al. 2017, Kobele et al. 2013 included (MaxT, SumT, SumS). Other information provided by the parser are the total number of operations used to build the final structure, the categorial GRAMMATICA/UNGRAMMATICAL prediction (based on failure in agreement, unfulfilled expectations or items pending in memory at the end of the derivation) and a Relativized Minimality complexity estimation (RelM) based on feature sharing while elements are stored in memory and their difficulty at retieval (Chesi Canal 2019)

FIXME
------------------
- lexicon should be implemented with TRIE (Chesi 2019, Stabler 2013)
- memory structure should be implemented with TRIE <- blocking RelM full measure implementation
- Derivation tree must be created by (deep)copying nodes: features are destroyed when succesfull structure building operations apply, then in this format the node is a bit "flat" and dependency-like
- parameterization must be fully expanded (late expansion, pied-piping and expectation stacking, see Chesi & Brattico 2018)

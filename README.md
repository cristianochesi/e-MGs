# e-MGs
Expectation-based Minimalist Grammars (v 1.0)
===================================================

This is a simple Python3 implementation of the expectation-based Minimalist Grammars (e-MGs) discussed in Chesi 2021.
E-MGs are greatly indebted with MGs (Stabler 1997) and PMGs (Chesi 2007, 2017) formalisms.
This implementation includes: a grammar definition, a unified parsing/generation interactive procedure, a set of parameterizations and lexica dealing with specific formal (e.g., counting recursion) and linguistic facts (copular constructions in Italian, relative clauses in English, Greenberg's Universal 20 re-ordering etc.), few simple complexity metrics both producing on-line (word-by-word) encoding integration and retrieval costs and off-line (global) costs.


Background
----------

e-MGs are simplifications of both MGs Stabler (1997) and PMGs (Chesi 2007, 2017).
In a nutshell, Merge is expectation-based, that is, each category (X) must be selected by a superordinate node with the relevant expectation associated to it in the lexicon (=X).
This simple mechanism is sufficient to dispense the grammar from probe-goals/licensee-licensors features to deal with non-local dependencies:
Items with unexpected categories simply get moved in the Memory-buffer of the superordinate node and transmitted to sequential phases (i.e., last-selected expectations).
Items selected while the superordinate node has other selection features qualifies as "nested phases" and cannot receive any pending item (unless they become sequential at some point of the derivation and "late expansion" of selection is permitted by parsing parameterization).

The off-line complexity metrics are simple translations of the one proposed in Gerth 2017, Graf et al 2017, Kobele 2013 and used in various works (e.g., De Santo 2019).
On-line metrics are simplified versions of the metrics discussed in Chesi & Canal 2019.

- Bianchi Valentina, Cristiano Chesi (2006): [Phases, Left Branch Islands, and Computational Nesting](https://repository.upenn.edu/pwpl/vol12/iss1/3/)
- Chesi Cristiano (2021): [Expectation-based Minimalist Grammars](https://lingbuzz.net/lingbuzz/006135)
- Chesi Cristiano (2019): [An efficient Trie for binding (and movement)](http://ceur-ws.org/Vol-2253/paper07.pdf)
- Chesi Cristiano (2017): [Phase-based Minimalist Parsing and complexity in non-local dependencies](http://ceur-ws.org/Vol-2006/paper014.pdf)
- Chesi Cristiano (2007): [An introduction to Phase-based Minimalist Grammars: why move is Top-Down from Left-to-Right](http://www.ciscl.unisi.it/doc/doc_pub/chesi-2007-PMG-intro-STIL_vol1.pdf)
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
To run the "generate" procedure, execute this file in your Python shell (or run `Python3 <what follows>` or `Python <what follows>` from command line):

e.g. `eMG_start.py -i "a a a b b b" -l lexicon\PMG_dict_ab.json -p parameters\PMG_param_default.json` 
  (notice that ambiguity must be resolved in-line)

Few examples to test specific constructions.
- Canonical copular constructions (Italian lexicon):

`eMG_start.py -i "le foto del muro sono la causa della rivolta" -l lexicon\PMG_dict_copular_ita.json -p parameters\PMG_param_ita.json`
- Inverse copular constructions (Italian lexicon), change the -i option above with:

`-i "la causa della rivolta sono le foto del muro"`
- Subject Relative (English lexicon):

`eMG_start.py -i "I saw the giraffe that kicked the cow" -l lexicon\eMG_dict_RC.json -p parameters\eMG_param_default.json`
- Object Relative, change the -i option above with:

`-i "I saw the giraffe that the cow kicked"`
- Object Relative + embedding, change the -i option above with:

`-i "the giraffe that the cow kicked smiled"`

`eMG_start.py` gets an input string `-i`, a lexicon file in json format `-l` and a parameter set `-p`. Simple lexica are provided to test the capabilities of the grammar (`PMG_dict_ab.json` implement counting recursion, `PMG_dict_RC.json` simple examples of Relative Clauses in English, `PMG_dict_copular_ita` include some classic example of subectraction from copular sentences etc.).
Also parameterization files (json format) are provided as example, one default `PMG_param_default.json` with no special parameterization, and two specifying mandatory agreement categories in Italian and English (unification algorithm to be implemented).

`eMG_grammar.py` implements the basic Merge, Move and Agree structure building operations as well as the Select function (lexical retrieval).

`eMG_generate.py` implements the basic Top-Down structure building algorithm (lexical ambiguity is resolved by asking the user to pick up a relevant item among the ones compatible). The procedure is equivalent in Parsing and Generation: both in parsing and in generation the input string must be considered feeding the algorithm on a word-by-word pace. Play with ambiguity and knowledge asymmetries between the speaker and the listener to resolve the ambiguity and see the difference in terms of complexity

`eMG_complexity_metrics.py` implements the basic set of complexity metrics (both on-line - word-by-word - and off-line - possible correlation to general acceptability/grammaticality)

`eMG_tree.py` implements a useful function print_node(MG_done) that prints the tree in LATEX-FOREST format as in Kobele et al. 2013, Graf et al. 2017 (this is a compact dependency-like tree)

`eMG_utilities.py` provide utilities to deal with Nodes search, tree and complexity metrics printing

Complexity Metrics
------------------
Basic complexity Metrics inspired by Graf et al. 2017, Kobele et al. 2013 included (MaxT, SumT, SumS). 
Other information provided by the parser are the total number of operations used to build the final structure, the categorial GRAMMATICAL/UNGRAMMATICAL prediction (based on failure in agreement, unfulfilled expectations or items pending in memory at the end of the derivation) and a Relativized Minimality complexity estimation (RelM) based on feature sharing while elements are stored in memory and their difficulty at retieval (see FREC in Chesi & Canal 2019).

FIXME
------------------
- lexicon should be implemented using TRIE-like structure (Chesi 2019, Stabler 2013)
- memory structure should be implemented using TRIE-like structure <- better RelM full measure implementation
- Constituency tree must be created by (deep)copying nodes: features are destroyed when successful structure building operations apply, then, in this format, the structure appears to be a bit too "flat" and dependency-like (indexes however unambiguously tell us in which order the items are processed)
- parameterization should be expanded (anti-locality, pied-piping and expectation stacking, see Chesi & Brattico 2018)

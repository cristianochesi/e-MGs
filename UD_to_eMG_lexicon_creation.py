import getopt
import sys

from eMG_generate import *

global UD_dict
global lexicon_file

silent = False
tokens = 0
types = 0
ambiguous_tokens = 0
ambiguous_tokens_lexical = 0
ambiguous_tokens_morphological = 0
ambiguous_tokens_dependency = 0
dep_total = 0
dep_backward = 0
dep_backward_local = 0
sentence = []
expect = {}
dep = {}


def write_lexicon(lexicon):
	mk = list(lexicon.keys())
	mk.sort()
	sorted_lexicon = {i: lexicon[i] for i in mk}

	json_string = json.dumps(sorted_lexicon)
	json_string = json_string.replace("},", "},\n")
	with open(lexicon_file, 'w') as outfile:
		outfile.write(json_string)
		print("Tokens processed: ", tokens, "\nLexicon size: ", types, " distinct types\nAmbiguous tokens: ", ambiguous_tokens, " (Lexical ambiguity ratio: ", ambiguous_tokens / tokens, ")")
		print("Lexical ambiguity: ", ambiguous_tokens_lexical / ambiguous_tokens, " - Morphological ambiguity: ", ambiguous_tokens_morphological / ambiguous_tokens, " - Ambigous dependencies: ", ambiguous_tokens_dependency / ambiguous_tokens)
		print("Number of dependencies: ", dep_total, "Backward dependencies: ", dep_backward, "(",dep_backward/dep_total, "of the total; local ratio:", dep_backward_local/dep_backward, ")")


def add_lex_items():
	global tokens
	global types
	global ambiguous_tokens
	for word_tagged in sentence:
		tokens = tokens + 1
		items = word_tagged.split("\t")
		if UD_dict.get(items[1].lower()):
			if ambiguous(items):
				ambiguous_tokens = ambiguous_tokens + 1
		else:
			types = types + 1
			agr = get_agree_features(items)
			if items[6] == "0":
				UD_dict.update({"ROOT": {"label": [{"0": "ROOT"}], "expected": [{}], "expect": [{"0": items[3]}], "dep": "", "agree": ""}})
			else:
				get_dependencies(items)
			UD_dict.update({items[1].lower(): {"label": [{"0": items[3]}], "expected": [{"0": items[3]}], "expect": [{}], "dep": [{}], "agree": agr}})
			UD_dict[items[1].lower()].update({"expect": [expect]})
			UD_dict[items[1].lower()].update({"dep": [dep]})
			if not silent:
				print("lexical item added: ", items)


def get_dependencies(it):
	deps = 0
	global dep_backward
	global dep_backward_local
	global dep_total
	global expect
	global dep
	expect = {}
	dep = {}
	if it[6] != "0":
		for wt in sentence:
			items_dep = wt.split("\t")
			if items_dep[6] == it[0]:
				expect.update({deps: items_dep[3]})
				dep.update({deps: items_dep[7]})
				deps += 1
				dep_total += 1
				if int(it[0]) > int(items_dep[0]):
					dep_backward += 1
					if int(it[0]) == int(items_dep[0])+1:
						dep_backward_local += 1


def ambiguous(items):
	global ambiguous_tokens_lexical
	global ambiguous_tokens_morphological
	global ambiguous_tokens_dependency
	agree_features = get_agree_features(items)
	ambiguity = False
	if UD_dict.get(items[1].lower()).get("expected")[0].get("0") != items[3]:
		if not silent:
			print("-", items[1].lower(), "- is lexically ambiguous", UD_dict.get(items[1].lower()).get("expected")[0].get("0"), items[3])
		ambiguous_tokens_lexical += 1
		ambiguity = True
	elif UD_dict.get(items[1].lower()).get("agree") != agree_features:
		if not silent:
			print("-", items[1].lower(), "- is morphologically ambiguous")
		ambiguous_tokens_morphological += 1
		ambiguity = True
	elif UD_dict.get(items[1].lower()).get("expect") is not None:
		get_dependencies(items)
		if (expect != UD_dict.get(items[1].lower()).get("expect")[0]) and (dep != UD_dict.get(items[1].lower()).get("dep")[0]):
			if not silent:
				print("-", items[1].lower(), "- establish ambiguous dependencies")
			ambiguous_tokens_dependency += 1
			ambiguity = True
	return ambiguity


def get_agree_features(items):
	agree_features = items[5].split("|")
	feature = ""
	feature_n = 0
	if agree_features[0] != "_":
		for f in agree_features:
			value = f.split("=")
			if feature_n != 0:
				feature += "."
			feature_n += 1
			feature += value[1]
	return feature


def main(argv):
	global lexicon_file
	global silent
	lexicon_file = 'lexicon/eMG_UD_extracted.json'
	input_treebank = ''

	try:
		opts, args = getopt.getopt(argv, "si:", ["silent", "input_sentences="])
	except getopt.GetoptError as e:
		sys.stderr.write("%s %s\n" % (argv[0], e.msg))
		sys.exit(1)
	for opt, arg in opts:
		if opt == '-h':
			print('UD_to_eMG_lex_extraction.py -i <input file in CONLLU format you want to use to create your eMG lexicon>')
			sys.exit()
		elif opt in ("-i", "--input_treebank"):
			input_treebank = arg
		elif opt in ("-s", "--silent"):
			silent = True

	print('Input: "' + input_treebank + '"')
	print('Lexicon file: ', lexicon_file)

	global UD_dict
	UD_dict = dict()

	sentences = open(input_treebank, "r", encoding="utf-8")
	global sentence
	sentence = []

	for line in sentences:
		if line == "\n":
			if sentence:
				add_lex_items()
			sentence = []
		elif not line[0] == "#" and line[0]:
			sentence.append(line)

	write_lexicon(UD_dict)


if __name__ == "__main__":
	main(sys.argv[1:])

import getopt
import sys

from eMG_generate import *

agree_cats = []
late_expand = []
late_expand_default = False


def main(argv):
	global agree_cats
	global late_expand
	global late_expand_default

	lexicon_file = 'lexicon/eMG_dict_RC.json'
	parameters_file = 'parameters/eMG_param_default.json'
	input_sentence = "I saw the cow that the giraffe kicked"

	try:
		opts, args = getopt.getopt(argv, "i:l:p:", ["input_sentence=", "lexicon_file=", "parameters_file="])
	except getopt.GetoptError as e:
		sys.stderr.write("%s %s\n" % (argv[0], e.msg))
		sys.exit(1)
	for opt, arg in opts:
		if opt == '-h':
			print('eMG_start.py -i <input sentence you want to process> -l <lexicon_file.json> -p <parameters_file.json>')
			sys.exit()
		elif opt in ("-i", "--input_sentence"):
			input_sentence = arg
		elif opt in ("-l", "--lexicon_file"):
			lexicon_file = arg
		elif opt in ("-p", "--parameters_file"):
			parameters_file = arg

	print('Input: "' + input_sentence + '"')
	print('Lexicon file: ', lexicon_file)
	print('Parameter file: ', parameters_file)

	g = PMG_generate(lexicon_file)
	root = g.mg.select("ROOT")
	if root.ambiguous:
		prompt = "Digit your ROOT choice:\n"
		for i, r in enumerate(root.ambiguous):
			prompt = prompt + "[" + str(i) + "] for " + r + "\n"
		choice = input(prompt)
		while not check_choice(choice, len(root.ambiguous)):
			choice = input("Wrong choice. " + prompt)
		root = g.mg.select(root.ambiguous[int(choice)])
	g.mg.set_root(root)
	get_param(parameters_file)
	g.mg.set_param_agree(agree_cats)
	g.mg.set_late_expansion(late_expand)
	g.mg.late_expansion_default = late_expand_default
	g.sentence = input_sentence
	g.generate(input_sentence.split())


def get_param(param_file) -> {}:
	global agree_cats
	global late_expand
	global late_expand_default

	with open(param_file) as json_file:
		params = json.load(json_file)
	n = 0
	for x in params['Agreement']['expected'][0]:
		agree_cats.insert(n, params['Agreement']['expected'][0][x])
		n += 1
	n = 0
	for x in params['Late_expansion']['expected'][0]:
		late_expand.insert(n, params['Late_expansion']['expected'][0][x])
		n += 1
	late_expand_default = bool(params['Late_expansion']['default'])


if __name__ == "__main__":
	main(sys.argv[1:])

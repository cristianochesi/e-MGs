import getopt
import sys

from PMG_generate import *


def main(argv):
	# input_sentence = 'the child likes Mary'
	# task = "parsing"
	# lexicon_file = 'PMG_dict_SVO_eng.json'
	# parameters_file = 'PMG_param_eng.json'
	# input_sentence = 'quali foto sono la causa'
	# input_sentence = 'la causa della rivolta pro sono le foto del muro'
	# lexicon_file = 'PMG_dict_copular_inverse_ita.json'
	# input_sentence = 'le foto del muro sono la causa della rivolta'
	# lexicon_file = 'PMG_dict_copular_ita.json'
	# parameters_file = 'PMG_param_ita.json'

	# input_sentence = 'a a b b'
	# lexicon_file = 'PMG_dict_ab.json'
	# parameters_file = 'PMG_param_default.json'

	lexicon_file = 'lexicon/PMG_dict_RC.json'
	parameters_file = 'parameters/PMG_param_default.json'
	input_sentence = "I saw the cow that the giraffe kicked"
	# input_sentence = "I saw the giraffe that kicked the cow"
	# input_sentence = "the giraffe that the cow kicked smiled"

	input_sentence = "the giraffe that I saw smiled"

	try:
		opts, args = getopt.getopt(argv, ["input=", "task=", "lexicon_file=", "parameters_file="])
	except getopt.GetoptError:
		print('PMG_start.py -i <input sentence (parsing) or category (generation) you want to process> -t <parsing|generation> -l <lexicon_file.json> -p <parameters_file.json>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('PMG_start.py -i <input sentence (parsing) or category (generation) you want to process> -t <parsing|generation> -l <lexicon_file.json> -p <parameters_file.json>')
			sys.exit()
		elif opt in ("-i", "--input"):
			input_sentence = arg
		elif opt in ("-t", "--task"):
			task = arg
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
	g.mg.set_param_agree(get_param(parameters_file))
	g.sentence = input_sentence
	g.generate(input_sentence.split())


def get_param(param_file) -> []:
	agree_cats = []
	with open(param_file) as json_file:
		params = json.load(json_file)
	n = 0
	for x in params['Agreement']['expected'][0]:
		agree_cats.insert(n, params['Agreement']['expected'][0][x])
		n += 1
	return agree_cats


if __name__ == "__main__":
	main(sys.argv[1:])

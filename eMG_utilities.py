import copy

from eMG_complexity_metrics import *


def print_offline_measures(t):
	# fixme: to be expanded
	print("\n---Offline-Measures------")
	print("Sentence: " + t.sentence)
	print("Steps: " + str(t.step))
	print("Pending items im mem: " + str(len(t.mg.current_node.mem)))
	if t.merge_failed:
		print("Pending word (failed to merge): " + t.merge_failed_word)
	print("Pending expectations: " + str(t.mg.current_node.get_expect()))
	if len(t.mg.current_node.mem) == 0 and t.mg.current_node.get_expect() == "" and len(t.words) == 0 and not t.merge_failed:
		print("Prediction: GRAMMATICAL")
	else:
		print("Prediction: UNGRAMMATICAL")
	print("Merge unexpected items: " + str(t.mg.merge_unexpected))
	print("Move failures: " + str(get_move_failures()))
	print("Ambiguities: " + str(get_MaxD()))
	print("MaxD: " + str(get_MaxD()))
	print("MaxT: " + str(get_MaxT()))
	print("SumT: " + str(get_SumT()))
	print("MaxS: " + str(get_MaxS()))
	print("RelM: " + str(get_RelM()))


def print_online_measures(t):
	print("\n---Online-Measures------")
	# words = t.sentence.split()
	words = t.words_disambiguated
	print("Sentence:\t", end='')
	for word in words:
		print(word + "\t", end='')
	print("\nENCODING:\t", end='')
	nodes = copy.deepcopy(t.nodes)
	for word in words:
		cw = find_word(nodes, word)
		print(str(cw.encoding) + "\t", end='')
	print("\nINTEGRATION:\t", end='')
	nodes = copy.deepcopy(t.nodes)
	pw = eMG_node.PMG_node("", [], [], [], "")
	pw.index = 0
	for word in words:
		cw = find_word(nodes, word)
		enc = cw.index - pw.index
		pw = cw
		print(str(enc) + "\t", end='')
	print("\nRETRIEVAL:\t", end='')
	nodes = copy.deepcopy(t.nodes)
	for word in words:
		print(str(get_retrieval_cost(nodes, word)) + "\t", end='')
	print("\nINTERVENTION:\t", end='')
	nodes = copy.deepcopy(t.nodes)
	for word in words:
		print(str(get_intervention_cost(nodes, word)) + "\t", end='')


def find_word(nodes, word):
	node = eMG_node.PMG_node("", [], [], [], "")
	for n in range(0, len(nodes)):
		if nodes[n].phon == word:
			node = nodes[n]
			nodes.pop(n)
			break
	return node


def print_tree(t):
	print("\n---Tree------------------")
	print("\\begin{forest}")
	t.tree.print_node(t.mg.root)
	t.tree.print_annotations()
	print("\\end{forest}")


def check_choice(choice, size):
	check = True
	try:
		i = int(choice)
		if i >= size:
			check = False
	except ValueError:
		check = False
	return check

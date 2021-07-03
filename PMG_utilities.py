import copy
import math
from PMG_complexity_metrics import *


def print_offline_measures(t):
	# fixme: to be expanded
	print("\n---Offline-Measures------")
	print("Sentence: " + t.sentence)
	print("Steps: " + str(t.step))
	print("Pending items im mem: " + str(len(t.mg.current_node.mem)))
	print("Pending expectations: " + str(t.mg.current_node.get_expect()))
	if len(t.words) > 0:
		print("Pending words: " + str(len(t.words)) + " are not integrated; first one failed to merge was '" + t.words[0] + "'")
	if len(t.mg.current_node.mem) == 0 and t.mg.current_node.get_expect() == "" and len(t.words) == 0:
		print("Prediction: GRAMMATICAL")
	else:
		print("Prediction: UNGRAMMATICAL")
	print("Move failures: " + str(get_move_failures()))
	print("Ambiguities: " + str(get_MaxD()))
	print("MaxD: " + str(get_MaxD()))
	print("MaxT: " + str(get_MaxT()))
	print("SumT: " + str(get_SumT()))
	print("MaxS: " + str(get_MaxS()))
	print("RelM: " + str(get_RelM()))


def print_online_measures(t):
	print("\n---Online-Measures------")
	words = t.sentence.split()
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
	pw = PMG_node.PMG_node("", [], [], [], "")
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


def find_word(nodes, word):
	node = PMG_node.PMG_node("", [], [], [], "")
	for n in range(0, len(nodes)):
		if nodes[n].phon == word:
			node = nodes[n]
			nodes.pop(n)
			break
	return node


def get_retrieval_cost(nodes, word):
	retrieval = 0
	for n in range(0, len(nodes)):
		if nodes[n].phon == word:
			if len(nodes[n].children) >= 1:
				for child in nodes[n].children:
					if child.phon.startswith("$t"):
						# print(child.phon + ": " + str(child.mem_outdex) + " - " + str(child.mem_index))
						retrieval += round(math.log(child.mem_outdex - child.mem_index)*len(nodes[n].children), 2)
	return retrieval


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

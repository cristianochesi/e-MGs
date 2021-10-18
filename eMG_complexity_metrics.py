import eMG_node
import math

maxD = 0
maxT = 0
maxS = 0
sumT = 0
relM = 0
move_failures = 0
ambiguities = 0


def get_MaxT() -> int:
	global maxT
	return maxT


def get_MaxD() -> int:
	global maxD
	return maxD


def get_MaxS() -> int:
	global maxS
	return maxS


def get_SumT() -> int:
	global sumT
	return sumT


def get_RelM() -> int:
	global relM
	return relM


def get_move_failures() -> int:
	global move_failures
	return move_failures


def get_ambiguities() -> int:
	global ambiguities
	return ambiguities


def get_retrieval_cost(nodes, word):
	retrieval = 0
	for n in range(0, len(nodes)):
		if nodes[n].phon == word:
			if len(nodes[n].children) >= 1:
				for child in nodes[n].children:
					if child.phon.startswith("$t"):
						retrieval += round(math.log(child.mem_outdex - child.mem_index), 2)
	return retrieval


def get_intervention_cost(nodes, word):
	intervention = 0
	for n in range(0, len(nodes)):
		if nodes[n].phon == word:
			intervention += nodes[n].retrieval
	return intervention


def set_MaxT(node: eMG_node):
	global maxT
	t = node.outdex - node.index
	if maxT < t:
		maxT = t


def set_SumT(node: eMG_node):
	global sumT
	t = node.outdex - node.index
	if t > 1:
		sumT += t


def set_MaxS(node: eMG_node):
	global maxS
	t = node.mem_outdex - node.mem_index
	if maxS < t:
		maxS = t


def set_MaxD(node: eMG_node):
	global maxD
	if node.nesting_level > maxD:
		maxD = node.nesting_level


def set_AgreeMismatch(node: eMG_node):
	print("\t\tAgreement mismatch penalty considered for encoding (+1) at node '" + node.phon + "'")
	node.encoding += 1


def set_FRC(node: eMG_node):  # minimal implementation of Chesi (2017) Feature Retrieval Cost (FRC); only top-most accessible features are considered (e.g. D-related features instead of D and N related features as in Chesi & Canal 2019)
	global relM
	if len(node.mem) >= 1:
		dF = cued_features(node.mem[0], node)
		nF = shared_features(node)
		rM = round(pow(1 + nF, len(node.mem)) / (1 + dF), 2)
		if node.retrieval == 0:
			node.retrieval = 1
		node.retrieval *= rM
	print("\t\tFRC calculated: dF=" + str(dF) + " nF=" + str(nF) + " FRC= " + str(rM))
	if rM > relM:
		relM = rM


def set_encoding(node: eMG_node):
	for label in node.label:
		if label == "N" or label == "V":
			node.encoding += 1


def add_encoding_penalty(node: eMG_node):
	node.encoding += 1


def add_move_failure():
	global move_failures
	move_failures += 1


def add_ambiguity():
	global ambiguities
	ambiguities += 1


def cued_features(retrieved: eMG_node, retrieving: eMG_node):
	cF = 0
	if retrieved.get_expect() == retrieving.get_expect():
		cF = 1
	agreeF = retrieving.agree.split(".")
	agreedF = retrieved.agree.split(".")
	for x in agreeF:
		for y in agreedF:
			if x == y:
				cF += 1
	return cF


def shared_features(retrieving: eMG_node):
	nF = 0
	i = 0
	items = []
	for m in retrieving.mem:
		if i > 0:
			items.append(m)
		i += 1
	for n in items:
		if retrieving.get_expect() == n.get_expect():
			nF = 1
		agreeF = retrieving.agree.split(".")
		agreedF = n.agree.split(".")
		for x in agreeF:
			for y in agreedF:
				if x == y:
					nF += 1
	return nF

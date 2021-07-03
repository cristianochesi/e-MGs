import PMG_node

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


def set_MaxT(node: PMG_node):
	global maxT
	t = node.outdex - node.index
	if maxT < t:
		maxT = t


def set_SumT(node: PMG_node):
	global sumT
	t = node.outdex - node.index
	if t > 1:
		sumT += t


def set_MaxS(node: PMG_node):
	global maxS
	t = node.mem_outdex - node.mem_index
	if maxS < t:
		maxS = t


def set_MaxD(node: PMG_node):
	global maxD
	if node.nesting_level > maxD:
		maxD = node.nesting_level


def set_RelM(node: PMG_node):
	global relM
	set_retrieval(node)
	expected = ""
	if len(node.mem) > 1:
		for n in node.mem:
			if not expected:
				expected = n.get_expected()
			else:
				if expected == n.get_expected():
					relM += 1


def set_encoding(node: PMG_node):
	for label in node.label:
		if label == "N" or label == "V":
			node.encoding = 1


def set_retrieval(node: PMG_node):
	expected = ""
	if len(node.mem) > 1:
		for n in node.mem:
			if not expected:
				expected = n.get_expected()
			else:
				if expected == n.get_expected():
					node.retrieval = 1


def add_move_failure():
	global move_failures
	move_failures += 1


def add_ambiguity():
	global ambiguities
	ambiguities += 1

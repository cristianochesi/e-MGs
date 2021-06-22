def remove_expect(node):
	return node.expect.pop(0)


def remove_expected(node):
	return node.expected.pop(0)


def print_measures(p):
	# fixme: to be expanded
	print("\n---Measures--------------")
	print("Steps: " + str(p.step))
	print("Pending items im mem: " + str(len(p.mg.current_node.mem)))
	print("Pending expectations: " + str(p.mg.current_node.get_expect()))
	if len(p.words) > 0:
		print("Pending words: " + str(len(p.words)) + " are not integrated; first one failed to merge was '" + p.words[0] + "'")
	if len(p.mg.current_node.mem) == 0 and p.mg.current_node.get_expect() == "" and len(p.words) == 0:
		print("Prediction: GRAMMATICAL")
	else:
		print("Prediction: UNGRAMMATICAL")
	print("MaxD: " + str(p.maxD))
	print("Move failures: " + str(p.move_failures))
	print("MaxT: " + str(p.maxT))
	print("MaxS: " + str(p.maxS))
	print("RelM: " + str(p.relM))


def print_tree(p):
	print("\n---Tree------------------")
	p.tree.print_node(p.mg.root)
	p.tree.print_annotations()

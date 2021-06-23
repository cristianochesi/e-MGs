def remove_expect(node):
	return node.expect.pop(0)


def remove_expected(node):
	return node.expected.pop(0)


def print_measures(t):
	# fixme: to be expanded
	print("\n---Measures--------------")
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
	print("MaxD: " + str(t.maxD))
	print("Move failures: " + str(t.move_failures))
	print("MaxT: " + str(t.maxT))
	print("SumT: " + str(t.sumT))
	print("MaxS: " + str(t.maxS))
	print("RelM: " + str(t.relM))


def print_tree(t):
	print("\n---Tree------------------")
	t.tree.print_node(t.mg.root)
	t.tree.print_annotations()


def check_choice(choice, size):
	check = True
	try:
		i = int(choice)
		if i >= size:
			check = False
	except ValueError:
		check = False
	return check


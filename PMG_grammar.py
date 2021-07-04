import json

from PMG_complexity_metrics import *
from PMG_utilities import *


# fixme: implement antilocality?
# fixme: implement ambiguous element selection (DONE in generation)
# fixme: implement referential buffer and binding (Schlenker Bianchi)

def is_mem_empty(node: PMG_node) -> bool:
	if len(node.mem) == 0:
		return True


def is_phase_nested(expecting_node: PMG_node) -> bool:
	if expecting_node.has_expect() or expecting_node.has_expected() is None:
		return True
	else:
		return False


def sequential_phase_mem_transmission(last_phase: PMG_node, sequential_phase: PMG_node):
	if not is_mem_empty(last_phase):
		sequential_phase.mem = last_phase.mem
		last_phase.mem = []


def remove_expect(node):
	return node.expect.pop(0)


def remove_expected(node):
	return node.expected.pop(0)


def agree(cn: PMG_node, w: PMG_node) -> bool:
	# fixme: to be expanded using Unification
	if w.agree == "" or cn.agree == "" or cn.agree == w.agree:
		print("\t\tAGREE OK: [" + cn.agree + ", " + cn.phon + "] is compatible with " + w.agree + ", " + w.phon + "]")
		return True
	else:
		print("\t\tAGREE FAILED: [" + cn.agree + ", " + cn.phon + "] is incompatible with " + w.agree + ", " + w.phon + "]")
		return False


def move(cn: PMG_node, w: PMG_node):
	print("\t\tMOVE: M-buffering '" + w.phon + "' (label = " + w.name + ") phase with expected feature '" + w.get_expected() + "' in the phase '" + cn.get_label() + "'")
	m = copy.deepcopy(w)
	m.phon = "$t_{" + w.name + "}$"
	m.in_mem = True
	m.mem_index = w.index
	cn.mem.insert(0, m)


class PMG_grammar:
	root = None
	current_node = None
	step = 0
	agr_cats = []
	move_failures = 0
	nesting_level = 0
	previous_phases = []
	global_encoding = 0
	global_retrieval = 0
	n_words = 0
	words = []
	nodes = []
	word = None
	i = 0

	def __init__(self, lex):
		self.lex = {}
		with open(lex) as json_file:
			self.lex = json.load(json_file)

	# fixme:	trie = {v: k for k, v in self.lex['expected'].items()}	print(trie)

	def merge(self, cn: PMG_node, w: PMG_node) -> str:
		if cn.has_expect():
			if w.has_expected():
				if w.is_expected(cn.get_expect()):
					if cn.get_agree_requirement():
						if not agree(cn, w):
							return "Agreement failure"
					print("\t\tMERGE SUCCESS: [" + cn.phon + " =" + cn.get_expect() + " [" + w.get_expected() + " " + w.phon + "]]")
					remove_expect(cn)
					remove_expected(w)
					cn.children.append(w)
					# cn.attach(w) # fixme: arrange that function if you want to implement consituency-based trees
					w.parent = cn
					if cn.is_head_movement():
						cn.label.pop(0)
					if w.has_expected():
						move(cn, w)
					return "OK"
				elif not w.is_in_mem():
					cn.children.append(w)
					w.parent = cn
					if w.has_expected() and not w.is_in_mem():
						print("\t\tMERGE: expectation '" + cn.get_expect() + "' failed: missing feature '" + w.get_expected() + "'")
						move(cn, w)
					return "OK"
				return "item unexpected and already in MEM"
			else:
				print("\t\tMERGE: integration failed: '" + w.phon + "' does not have features to be expected ")
				return "nothing to be expected"
		elif not w.has_expected():
			if w.get_label() == "RC":
				#  fixme: PP and RC attachment problem
				#  get_relevant_superordinate_phase()
				rc_head = copy.deepcopy(cn)
				rc_head.phon = rc_head.name
				rc_head.expected.append("D")
				cn.children.append(w)
				w.parent = cn
				w.nesting_level = cn.nesting_level + 1
				move(w, rc_head)
				return "OK"
			return "MERGE: integration failed: '" + w.phon + "' cannot be selected and it is not an adjunct"
		else:
			print("\t\tMERGE: integration failed: '" + cn.phon + "' does not introduce any feature expectation")
			return "no further expectations"

	# fixme: implement trie and avoid LIFO memories

	def select(self, w) -> PMG_node:  # fixme: menage ambiguity by duplicating parse trees
		expect = []
		expected = []
		label = []
		ambiguous = []
		n = 0
		for x in self.lex[w]['expect'][0]:
			expect.insert(n, self.lex[w]['expect'][0][x])
			n += 1
		n = 0
		for x in self.lex[w]['expected'][0]:
			expected.insert(n, self.lex[w]['expected'][0][x])
			n += 1
		n = 0
		for x in self.lex[w]['label'][0]:
			label.insert(n, self.lex[w]['label'][0][x])
			n += 1
		if 'ambiguous' in self.lex[w]:
			n = 0
			for x in self.lex[w]['ambiguous'][0]:
				ambiguous.insert(n, self.lex[w]['ambiguous'][0][x])
				n += 1
		w_tagged = PMG_node.PMG_node(w, expect, expected, label, self.lex[w]['agree'])
		w_tagged.ambiguous = ambiguous
		if self.needs_agree(w_tagged):
			w_tagged.requires_agree = True
		w_tagged.index = 0
		w_tagged.outdex = 0
		return w_tagged

	def set_root(self, node: PMG_node):
		self.root = node
		self.current_node = self.root

	def phase_up(self, cn: PMG_node) -> bool:
		raise_up = True
		while not cn.has_expect():
			if cn.parent:
				self.current_node = cn.parent
				cn = self.current_node
			else:
				print("\t\tPHASE FAILURE: superordinate phase not available")
				raise_up = False
				break
		return raise_up

	def set_param_agree(self, nodes: []):
		self.agr_cats = nodes

	def needs_agree(self, node: PMG_node):
		for cat in self.agr_cats:
			if node.get_label() == cat:
				return True
		return False

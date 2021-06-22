from MG_tree import *
import MG_node
from MG_grammar import *
from MG_utilities import *


def is_mem_empty(node: MG_node) -> bool:
	if len(node.mem) == 0:
		return True


def is_phase_complete(node: MG_node) -> bool:
	if len(node.expect) == 0:
		return True


def is_phase_nested(expecting_node: MG_node) -> bool:
	if expecting_node.has_expect():
		return True
	else:
		return False


def sequential_phase_mem_transmission(last_phase: MG_node, sequential_phase: MG_node):
	if not is_mem_empty(last_phase):
		sequential_phase.mem = last_phase.mem
		last_phase.mem = []


class MG_parser:

	def __init__(self, lexicon):
		self.mg = MG_grammar(lexicon)
		self.tree = MG_tree()
		self.step = 0
		self.agr_cats = []
		self.move_failures = 0
		self.current_phase_level = 0
		self.maxD = 0
		self.maxT = 0
		self.maxS = 0
		self.numN = 0
		self.relM = 0
		self.words = []

	def parse(self, words):
		self.words = words
		print("\n---Derivation------------")

		while self.mg.current_node.has_expect():
			cn = self.mg.current_node
			self.step += 1
			cn.requires_agree = self.needs_agree(cn)
			print("step " + str(self.step) + ". Phase " + cn.get_label() + " - EXPECTING " + cn.get_expect())

			if len(cn.mem) > 0:
				for w_mem in cn.mem:
					self.step += 1
					print("step " + str(self.step) + ". attempting to MERGE item [" + cn.get_expect() + " " + cn.phon + "] with [" + w_mem.get_expected() + " " + w_mem.phon + "] from MEM")
					result = self.mg.merge(cn, w_mem)
					if result != "OK":
						print("\t\tMERGE FAILURE: " + result)
					if result == "OK":
						w_mem.mem_outdex = self.step
						w_mem.outdex = self.step
						self.tree.append_moved_child(w_mem) #  fixme
						if not w_mem.has_expected():
							cn.mem.pop(0)
					else:
						self.move_failures += 1

			if len(words) > 0:
				word = words.pop(0)
				self.step += 1
				w_tagged = self.select(word)
				w_tagged.index = self.step
				print("step " + str(self.step) + ". attempting to MERGE item [" + cn.get_expect() + " " + cn.phon + "] with [" + w_tagged.get_expected() + " " + w_tagged.phon + "]")
				result = self.mg.merge(cn, w_tagged)
				if result != "OK":
					print("\t\tMERGE FAILURE: " + result)
				if result == "OK":
					w_tagged.outdex = self.step
					if not w_tagged.has_expect():
						w_tagged.set_complete()
						while not is_phase_complete(cn):
							self.tree.print_node(cn)
							self.current_phase_level -= 1
							self.set_phase(cn.get_parent())
							cn = cn.get_parent()
					else:
						if is_phase_nested(w_tagged):
							sequential_phase_mem_transmission(cn, w_tagged)
							print("\t\t" + w_tagged.phon + " is a sequential phase, memory transmitted")
						cn = w_tagged
						self.current_phase_level += 1
						self.set_phase(cn)
				else:
					print("\t\tFAILED: word [" + w_tagged.get_expected() + " " + w_tagged.phon + "] cannot be accommodated with the current expectation")
			else:
				break

		print_measures(self)
		print_tree(self)

	def select(self, w) -> MG_node:
		expect = []
		expected = []
		label = []
		n = 0
		for x in self.mg.lex[w]['expect'][0]:
			expect.insert(n, self.mg.lex[w]['expect'][0][x])
			n += 1
		n = 0
		for x in self.mg.lex[w]['expected'][0]:
			expected.insert(n, self.mg.lex[w]['expected'][0][x])
			n += 1
		n = 0
		for x in self.mg.lex[w]['label'][0]:
			label.insert(n, self.mg.lex[w]['label'][0][x])
			n += 1

		w_tagged = MG_node(w, expect, expected, label, self.mg.lex[w]['agree'])

		if self.needs_agree(w_tagged):
			w_tagged.requires_agree = True

		if not w_tagged.has_expect():
			w_tagged.set_complete()

		return w_tagged

	def set_phase(self, node):
		self.mg.current_node = node
		if self.maxD < self.current_phase_level:
			self.maxD = self.current_phase_level

	def set_param_agree(self, nodes):
		self.agr_cats = nodes

	def needs_agree(self, node):
		for cat in self.agr_cats:
			if node.get_label() == cat:
				return True
		return False

	def set_root(self, node):
		self.mg.root = MG_node(node.phon, node.expect, node.expected, node.label, node.agree)
		self.mg.current_node = self.mg.root

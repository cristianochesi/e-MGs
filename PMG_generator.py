from PMG_grammar import *
from PMG_utilities import *
from PMG_tree import *
from PMG_node import *


def is_mem_empty(node: PMG_node) -> bool:
	if len(node.mem) == 0:
		return True


def is_phase_nested(expecting_node: PMG_node) -> bool:
	if expecting_node.has_expect():
		return True
	else:
		return False


def sequential_phase_mem_transmission(last_phase: PMG_node, sequential_phase: PMG_node):
	if not is_mem_empty(last_phase):
		sequential_phase.mem = last_phase.mem
		last_phase.mem = []


class PMG_generator:

	def __init__(self, lexicon):
		self.mg = PMG_grammar(lexicon)
		self.tree = PMG_tree()
		self.step = 0
		self.agr_cats = []
		self.move_failures = 0
		self.current_phase_level = 0
		self.maxD = 0
		self.maxT = 0
		self.sumT = 0
		self.maxS = 0
		self.numN = 0
		self.relM = "TBD"
		self.words = []
		self.sentence = ""

	def generate(self):
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
						w_mem.mem_outdex = copy.deepcopy(self.step)
						self.set_MaxS(w_mem)
						if not w_mem.has_expected():
							cn.mem.pop(0)
					else:
						self.move_failures += 1

			word = input("Next word: ")
			if not word == "END":
				w = self.select(word)
				if len(w.ambiguous) > 0:
					prompt = "'" + w.phon + "' is ambiguous, digit your disambiguation choice:\n"
					for i, r in enumerate(w.ambiguous):
						prompt = prompt + "[" + str(i) + "] for " + r + "\n"
					choice = input(prompt)
					while not check_choice(choice, len(w.ambiguous)):
						choice = input("Wrong choice. " + prompt)
					w = self.select(w.ambiguous[int(choice)])
			else:
				break

			self.sentence = self.sentence + " " + word

			self.step += 1
			print("step " + str(self.step) + ". attempting to MERGE item [" + cn.get_expect() + " " + cn.phon + "] with [" + w.get_expected() + " " + w.phon + "]")
			result = self.mg.merge(cn, w)
			if result != "OK":
				print("\t\tMERGE FAILURE: " + result)
				break
			elif result == "OK":
				w.index = copy.deepcopy(self.step)
				w.outdex = copy.deepcopy(self.step)
				cn.outdex = copy.deepcopy(self.step)
				self.set_MaxT(cn)
				self.set_SumT(cn)
				if not w.has_expect():
					while not cn.has_expect():
						self.current_phase_level -= 1
						if self.current_phase_level < 0:
							print("\t\tPHASE compete: root reached - " + cn.phon)
							break
						if cn.superordinate_phase:
							self.set_phase(cn.superordinate_phase)
							self.mg.current_node = cn.superordinate_phase
							cn = self.mg.current_node
						else:
							print("\t\tPHASE FAILURE: superordinate phase not available")
				else:
					if not is_phase_nested(cn):
						sequential_phase_mem_transmission(cn, w)
						print("\t\t" + w.phon + " is a sequential phase, memory transmitted")
					self.mg.current_node = w
					self.current_phase_level += 1
					self.set_phase(self.mg.current_node)
			else:
				print("\t\tFAILED: word [" + w.get_expected() + " " + w.phon + "] cannot be accommodated with the current expectation")

		print_measures(self)
		print_tree(self)  # fixme: nodes are modified/deleted during feature checking. To visualize a full tree, copies must be instantiated

	def select(self, w) -> PMG_node:
		expect = []
		expected = []
		label = []
		ambiguous = []
		n = 0
		a = ""
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
		try:
			a = self.mg.lex[w]['ambiguous']
		except KeyError:
			pass
		if a:
			n = 0
			for x in self.mg.lex[w]['ambiguous'][0]:
				ambiguous.insert(n, self.mg.lex[w]['ambiguous'][0][x])
				n += 1

		w_tagged = PMG_node(w, expect, expected, label, self.mg.lex[w]['agree'])
		w_tagged.ambiguous = ambiguous

		if self.needs_agree(w_tagged):
			w_tagged.requires_agree = True

		w_tagged.index = 0
		w_tagged.outdex = 0

		return w_tagged

	def set_phase(self, node):
		self.mg.current_node = node
		if self.maxD < self.current_phase_level:
			self.maxD = self.current_phase_level

	def set_param_agree(self, nodes: []):
		self.agr_cats = nodes

	def needs_agree(self, node: PMG_node):
		for cat in self.agr_cats:
			if node.get_label() == cat:
				return True
		return False

	def set_root(self, node: PMG_node):
		self.mg.root = node
		self.mg.current_node = self.mg.root

	def set_MaxT(self, node: PMG_node):
		t = node.outdex - node.index
		if self.maxT < t:
			self.maxT = t

	def set_SumT(self, node: PMG_node):
		t = node.outdex - node.index
		if t > 1:
			self.sumT = self.sumT + t

	def set_MaxS(self, node: PMG_node):
		t = node.mem_outdex - node.mem_index
		if self.maxS < t:
			self.maxS = t

	def set_RelM(self, node: PMG_node):
		self.relM = "TBD"  # fixme: to be defined based on a TRIE representation of MEM (the more categories you share in memory, the harder the retrieval

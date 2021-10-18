import copy


class PMG_node:

	def __init__(self, phon, expect, expected, label, agree):
		self.phon = phon
		self.expect = expect
		self.expected = expected
		self.agree = agree
		self.agree_checked = False
		self.requires_agree = False
		self.doubling = False
		self.late_expansion = False
		self.label = label
		self.name = "0"
		self.index = 0
		self.outdex = 0
		self.mem_index = 0
		self.mem_outdex = 0
		self.parent = None
		self.superordinate_phase = None
		self.nesting_level = 0
		self.children = []
		self.ambiguous = []
		self.mem = []
		self.ref = ""
		self.from_lex = False
		self.in_mem = False
		self.valued = True
		self.encoding = 0
		self.retrieval = 0

	def get_parent(self):
		return self.parent

	def has_parent(self):
		if self.parent:
			return True
		return False

	def get_parent_in_mem(self):
		node = self.parent
		while node.has_parent():
			for m in node.get_parent().mem:
				if m.ref == node.name:
					print("PARENT FOUND: " + m.ref)
					return m
			node = node.get_parent()
		return None

	def get_agree_requirement(self):
		return self.requires_agree

	def set_agree_requirement(self):
		self.requires_agree = True
		return self.requires_agree

	def is_in_mem(self):
		return self.in_mem

	def has_children(self) -> bool:
		if len(self.children) > 0:
			return True
		return False

	def get_children(self) -> list:
		return self.children

	def get_child(self) -> list:
		return self.children[0]

	def get_last_child(self) -> list:
		return self.children[-1]

	def has_expect(self) -> bool:
		if not len(self.expect) == 0:
			return True
		return False

	def is_expect(self, expected) -> bool:
		if self.expect[0] == expected:
			return True
		return False

	def get_expect(self):
		if self.has_expect():
			return self.expect[0]
		return ""

	def has_label(self):
		if len(self.label) > 0:
			return True
		return False

	def get_label(self):
		if self.has_label():
			return self.label[0]
		return ""

	def is_head_movement(self):
		if len(self.label) > 1:
			return True
		return False

	def has_expected(self) -> bool:
		if not len(self.expected) == 0:
			return True
		else:
			return False

	def is_expected(self, expect) -> bool:
		if self.expected[0] == expect:
			return True
		return False

	def is_next_expected(self, node) -> bool:
		if len(node.expect) > 1:
			if node.expect[1] == self.expected[0]:
				return True
		return False

	def delay_expect(self):
		if len(self.expect) > 1:
			pop = self.expect.pop(0)
			print("APPEND POP")
			self.get_parent_in_mem().mem.append(pop)

	def get_expected(self):
		if self.has_expected():
			return self.expected[0]
		else:
			return ""

	def has_children(self):
		if len(self.children) > 0:
			return True
		else:
			return False

	def is_last_child(self):
		if self.parent is not None:
			if self.parent.children[-1] == self:
				return True
			else:
				return False
		else:
			return False

	def is_sequential(self, node):
		if len(node.expect) == 1:
			self.is_expected(node)
			return True
		else:
			return False

	def check_any_other_expectation(self, node):
		while node.has_expect() and self.has_expected():
			if self.is_expected(node.get_expect()):
				print("\t\tOther expectation satisfied: [" + node.phon + ", " + node.get_expect() + "] [" + self.get_expected() + ", " + self.phon + "]")
				self.expected.pop(0)
				node.expect.pop(0)
			else:
				break

	def attach(self, node):
		node_copy = copy.deepcopy(self)
		node_copy.name = self.name + "_copy"
		self.substitute(node_copy)
		self.parent = node_copy
		node.parent = node_copy
		if self.has_expected():
			node_copy.children.append(node)
			node_copy.children.append(self)
		else:
			node_copy.children.append(self)
			node_copy.children.append(node)

	def substitute(self, node_copy):
		if self.has_parent():
			for n in self.parent.children:
				if n == self:
					print("substitution done:")
					print(n)
					print(node_copy)
					n = node_copy

from MG_node import *


class MG_tree:

	def __init__(self):
		self.indent = ""
		self.annotation = ""
		self.movement = ""

	def print_node(self, node: MG_node):
		if len(node.children) > 0:
			print(self.indent + "[" + node.phon + ", label=" + node.get_label() + " , name=" + node.name)
			self.annotation = self.annotation + "%\nnode[index] at (" + node.name + ") {" + str(node.index) + "};\nnode[outdex] at (" + node.name + ") {" + str(node.outdex) + "};\n"
			self.indent = self.indent + "\t"
			for child in node.children:
				self.print_node(child)
			print(self.indent + "]")
		else:
			print(self.indent + "[" + node.phon + ", label=" + node.get_label() + " , name=" + node.name + "]")
			if node.mem_outdex != 0:
				self.movement = self.movement + "\\draw[move = {canonical}] (" + str(node.inmem) + ") to[out = west, in =south west] (" + str(node.outmem) + ");\n"
		if node.is_last_child():
			self.indent = self.indent[1:]

	def print_annotations(self):
		print(self.movement)
		print(self.annotation)

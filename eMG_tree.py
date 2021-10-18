from eMG_node import *


class PMG_tree:

	def __init__(self):
		self.indent = ""
		self.annotation = ""
		self.movement = ""
		self.new_line = ""

	def print_node(self, node: PMG_node):
		if len(node.children) > 0:
			# print(self.indent + "[" + node.phon + ", label=" + node.get_label() + " , name=" + node.name) # fixme: better format with complete information, but remember to make deepcopies!
			print(self.indent + "[" + node.phon + ", name=" + node.name)
			self.annotation = self.annotation + "\n%\n\\node[index] at (" + node.name + ") {" + str(node.index) + "};\n\\node[outdex] at (" + node.name + ") {" + str(node.outdex) + "};"
			self.indent = self.indent + "\t"
			for child in node.children:
				self.print_node(child)
			print(self.indent + "]")
		else:
			# print(self.indent + "[" + node.phon + ", label=" + node.get_label() + " , name=" + node.name + "]") # fixme: better format with complete information, but remember to make deepcopies!
			print(self.indent + "[" + node.phon + " , name=" + node.name + "]")
			self.annotation = self.annotation + "\n%\n\\node[index] at (" + node.name + ") {" + str(node.index) + "};\n\\node[outdex] at (" + node.name + ") {" + str(node.outdex) + "};"
			if node.in_mem:
				if not self.movement == "":
					self.new_line = "\n"
				self.movement = self.movement + self.new_line + "\\draw[move = {canonical}] (" + str(node.mem_index) + ") to[out = south west, in = south west] (" + str(node.mem_outdex) + ");"
		if node.is_last_child():
			self.indent = self.indent[1:]

	def print_annotations(self):
		print(self.movement + self.annotation)

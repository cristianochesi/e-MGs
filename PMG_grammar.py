import json
import copy
from PMG_node import *
from PMG_utilities import *


class PMG_grammar:
	root = None
	current_node = None

	def __init__(self, lex):
		self.lex = {}
		with open(lex) as json_file:
			self.lex = json.load(json_file)

	def merge(self, cn: PMG_node, w: PMG_node) -> str:
		if cn.has_expect():
			if w.has_expected():
				if w.is_expected(cn.get_expect()):
					if cn.get_agree_requirement():
						if not self.agree(cn, w):
							return "agreement failed"
					print("\t\tMERGE SUCCESS: [" + cn.get_expect() + " " + cn.phon + " - " + w.get_expected() + " " + w.phon + "]")
					remove_expect(cn)
					remove_expected(w)
					w.superordinate_phase = cn
					cn.children.append(w)
					w.parent = cn
					if cn.is_head_movement():
						cn.label.pop(0)
					if w.has_expected() and not w.is_in_mem():
						self.move(cn, w)
					return "OK"
				else:
					print("\t\tMERGE: expectation '" + cn.get_expect() + "' failed: missing feature '" + w.get_expected() + "'")
					return "unexpected feature"
			else:
				print("\t\tMERGE: integration failed: '" + w.phon + "' does not have features to be expected ")
				return "nothing expectable"
		else:
			print("\t\tMERGE: integration failed: '" + cn.phon + "' does not introduce any feature expectation")
			return "no expectations"

	def agree(self, cn: PMG_node, w: PMG_node) -> bool:
		# fixme: to be expanded using Unification
		if w.agree == "" or cn.agree == "" or cn.agree == w.agree:
			print("\t\tAGREE OK: [" + cn.agree + ", " + cn.phon + "] is compatible with " + w.agree + ", " + w.phon + "]")
			return True
		else:
			print("\t\tAGREE FAILED: [" + cn.agree + ", " + cn.phon + "] is incompatible with " + w.agree + ", " + w.phon + "]")
			return False

	def move(self, cn: PMG_node, w: PMG_node):
		print("\t\tMOVE: M-buffering '" + w.phon + "' phase with expected feature '" + w.get_expected() + "' in the phase '" + cn.get_label() + "'")
		phon = "$t_{" + w.phon + " ...}$"
		m = PMG_node(phon, w.expect, w.expected, w.label, w.agree)
		m.label = w.get_expected()
		m.in_mem = True
		m.mem_index = w.outdex
		cn.mem.insert(0, m)

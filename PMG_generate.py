from PMG_grammar import *
from PMG_tree import *
from PMG_utilities import *


class PMG_generate:

	def __init__(self, lexicon):
		self.mg = PMG_grammar(lexicon)
		self.tree = PMG_tree()
		self.sentence = ""
		self.step = 0
		self.n_words = 0
		self.words = []
		self.nodes = []
		self.word = None

	def generate(self, words):
		self.words = words
		self.n_words = len(words)
		print("\n---Derivation------------")
		while self.mg.current_node.has_expect() or len(words) > 0:
			self.step += 1
			cn = self.mg.current_node
			cn.requires_agree = self.mg.needs_agree(cn)
			memory = ""
			mem_pops = []
			i = 0
			for m in cn.mem:
				memory += "[" + m.get_expected() + " " + m.phon + "]"
			print("step " + str(self.step) + ". Phase " + cn.get_label() + " - EXPECTING " + cn.get_expect() + " - MEM = <" + memory + ">")

			# fixme: antilocality should be excluded here
			for w_mem in cn.mem:
				self.step += 1
				print("step " + str(self.step) + ". attempting to MERGE item [" + cn.phon + " =" + cn.get_expect() + "] with [" + w_mem.get_expected() + " " + w_mem.phon + "] from MEM = <" + memory + ">")
				set_RelM(cn)
				result = self.mg.merge(cn, w_mem)
				if result != "OK":
					print("\t\tMERGE FAILURE: " + result)
					add_move_failure()
				else:
					self.nodes.append(w_mem)
					w_mem.name = str(self.step)
					w_mem.mem_outdex = copy.deepcopy(self.step)
					w_mem.outdex = copy.deepcopy(self.step)
					set_MaxS(w_mem)
					print("\t\tMERGE success: " + result)
					mem_pops.append(i)
				i += 1

			mem_pops.sort(reverse=True)
			for p in mem_pops:
				print("\t\tItem deleted from MEM: " + cn.mem[p].name)
				cn.mem.pop(p)

			if not self.word and len(words) > 0:
				self.word = words.pop(0)
				self.step += 1
				w = self.mg.select(self.word)
				if len(w.ambiguous) > 0:  # lexical ambiguity is simply resolved by asking which item to pick-up (as in generation)
					prompt = "'" + w.phon + "' is ambiguous, digit your disambiguation choice:\n"
					for i, r in enumerate(w.ambiguous):
						prompt = prompt + "[" + str(i) + "] for " + r + "\n"
					choice = input(prompt)
					while not check_choice(choice, len(w.ambiguous)):
						choice = input("Wrong choice. " + prompt)
					w = self.select(w.ambiguous[int(choice)])
					add_ambiguity()
				set_encoding(w)

			if self.word:
				pn = 0
				w.index = copy.deepcopy(self.step)
				w.name = str(copy.deepcopy(self.step))
				while pn <= len(self.mg.previous_phases):  # fixme: transform in a general function to attach adjuncts (not just Restrictive Relative clauses)
					if w.get_label() == "RC" and self.mg.previous_phases[pn].get_label() == "N":
						cn = self.mg.previous_phases[pn]
						break
					pn += 1
				print("step " + str(self.step) + ". attempting to MERGE item [" + cn.get_expect() + " " + cn.phon + "] with [" + w.get_expected() + " " + w.phon + "]")
				result = self.mg.merge(cn, w)
				if result != "OK":
					print("\t\tMERGE FAILURE: " + result)
					self.mg.phase_up(cn)
					while not self.mg.merge(cn, w) == "OK" and not cn.parent:
						print("\t\tPHASE UP: " + cn.phon)
						self.mg.phase_up(cn)
				if result == "OK":
					self.nodes.append(w)
					self.word = None
					i = copy.deepcopy(self.step)
					w.outdex = i
					w.mem_outdex = i
					cn.outdex = i
					set_MaxT(cn)
					set_SumT(cn)
					set_MaxD(cn)
					if not w.has_expect():
						self.mg.previous_phases.insert(0, w)
						self.mg.phase_up(cn)
					else:
						if not is_phase_nested(cn):
							sequential_phase_mem_transmission(cn, w)
							w.nesting_level += cn.nesting_level
							print("\t\t" + w.phon + " is a sequential phase, memory transmitted")
						else:
							w.nesting_level += cn.nesting_level + 1
						self.mg.current_node = w
				else:
					print("\t\tFAILED: word [" + w.get_expected() + " " + w.phon + "] cannot be accommodated with the current expectation")
			else:
				print("INPUT exhausted")

		print_offline_measures(self)
		print_online_measures(self)
		print_tree(self)  # fixme: nodes are modified/deleted during feature checking. To visualize a full tree, copies must be instantiated

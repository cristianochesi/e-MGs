from eMG_grammar import *
from eMG_tree import *
from eMG_utilities import *


class PMG_generate:

	def __init__(self, lexicon):
		self.mg = PMG_grammar(lexicon)
		self.tree = PMG_tree()
		self.sentence = ""
		self.step = 0
		self.words = []
		self.words_disambiguated = []
		self.nodes = []
		self.word = None
		self.merge_failed = False
		self.merge_failed_word = ""

	def generate(self, words):
		self.words = words
		w = None
		if self.mg.tracking:
			print("\n---Derivation------------")  																									# tracking
		while self.mg.current_node.has_expect() or len(words) > 0:
			if self.merge_failed:
				break
			self.step += 1
			cn = self.mg.current_node
			cn.requires_agree = self.mg.needs_agree(cn)
			memory = ""
			mem_pops = []
			i = 0
			if self.mg.tracking:
				for m in cn.mem:  																													# tracking
					memory += "[" + m.get_expected() + " " + m.phon  																				# tracking
					if m.has_expect():																												# tracking
						memory += " =" + m.get_expect()																								# tracking
					memory += "] "																													# tracking
				print("step " + str(self.step) + ". Phase " + cn.get_label() + " | EXPECTING " + cn.get_expect() + " | MEM = <" + memory + ">")  	# tracking

			for w_mem in cn.mem:  																												# todo: antilocality violations should be considered here
				if not w_mem.has_expect() or w_mem.is_sequential(cn):
					w_mem.late_expansion = False
					self.step += 1
					if self.mg.tracking:
						print("step " + str(self.step) + ". attempting to MERGE item [" + cn.phon + " =" + cn.get_expect() + "] with [" + w_mem.get_expected() + " " + w_mem.phon + "] from MEM = <" + memory + ">")  	# tracking
					result = self.mg.merge(cn, w_mem)
					if result != "OK":
						if self.mg.tracking:
							print("\t\tMERGE FAILURE: " + result)																					# tracking
						add_move_failure()
						if len(words) == 0:
							if not self.word:
								self.merge_failed = True
								self.merge_failed_word = self.word
					else:
						self.nodes.append(w_mem)
						self.merge_failed = False
						self.merge_failed_word = ""
						w_mem.name = str(copy.deepcopy(self.step))
						w_mem.mem_outdex = copy.deepcopy(self.step)
						w_mem.outdex = copy.deepcopy(self.step)
						w_mem.mem_outdex = copy.deepcopy(self.step)
						w_mem.outdex = copy.deepcopy(self.step)
						# w_mem.in_mem = False 																									# fixme: late expansion behaves incorrectly here if this check is activated
						set_MaxS(w_mem)
						set_FRC(cn)
						if self.mg.tracking:
							print("\t\tMERGE success: " + result)																					# tracking
						mem_pops.append(i)
						if w_mem.has_expect():
							self.mg.current_node = w_mem
					i += 1
			mem_pops.sort(reverse=True)
			for p in mem_pops:
				if self.mg.tracking:
					print("\t\tItem deleted from MEM: " + cn.mem[p].name)
				cn.mem.pop(p)

			if not self.word and len(words) > 0:																								# SCAN: retrieve lexical item(s) from the lexicon
				self.word = words.pop(0)
				self.step += 1
				w = self.mg.select(self.word)
				if self.mg.tracking:
					print("\t\tLexical retrieval of the word '" + self.word + "'")																# tracking
				if len(w.ambiguous) > 0:  																										# lexical ambiguity is simply resolved by asking which item to pick-up (= generation task)
					prompt = "'" + w.phon + "' is ambiguous, digit your disambiguation choice:\n"												# ambiguity resolution
					options = ""																												# ambiguity resolution
					for i, r in enumerate(w.ambiguous):																							# ambiguity resolution
						prompt = prompt + "[" + str(i) + "] for " + r + "\n"																	# ambiguity resolution
						options += "[" + str(i) + "] "																							# ambiguity resolution
					choice = input(prompt)																										# ambiguity resolution
					while not check_choice(choice, len(w.ambiguous)):																			# ambiguity resolution
						choice = input("Wrong choice. Options available: " + options + "\n" + prompt)											# ambiguity resolution
					w = self.mg.select(w.ambiguous[int(choice)])																				# ambiguity resolution
					add_ambiguity()
					add_encoding_penalty(w)
					if self.mg.tracking:
						print("encoding penalty of ambiguous item for '" + w.phon + "'")
				set_encoding(w)
				self.words_disambiguated.append(w.phon)

			if w and w != cn and w.from_lex:
				pn = 0
				w.index = copy.deepcopy(self.step)
				w.name = str(copy.deepcopy(self.step))
				while pn <= len(self.mg.previous_phases):
					if w.get_label() == "RC" and self.mg.previous_phases[pn].get_label() == "N":												# fixme: this only implements local/low attachment of Restrictive Relative clauses analysis and it is relevant for head initial languages
						cn = self.mg.previous_phases[pn]
						break
					pn += 1
				if self.mg.tracking:
					print("step " + str(self.step) + ". attempting to MERGE item [" + cn.phon + " =" + cn.get_expect() + "] with [" + w.get_expected() + " " + w.phon + "]")  # tracking
				result = self.mg.merge(cn, w)
				if result != "OK":
					if self.mg.tracking:
						print("\t\tMERGE FAILURE: " + result)																						# tracking
					while not result == "OK":
						if cn.has_parent():
							cn = cn.parent
							result = self.mg.merge(cn, w)
						else:
							if self.mg.tracking:
								print("\t\tMERGE FAILURE (after phase up): " + result)																				# tracking
							break
				if result == "OK":
					self.nodes.append(w)
					self.word = None
					self.merge_failed = False
					self.merge_failed_word = ""
					w.from_lex = False
					i = copy.deepcopy(self.step)
					w.outdex = i
					w.mem_outdex = i
					cn.outdex = i
					set_MaxT(cn)
					set_SumT(cn)
					set_MaxD(cn)
					if not w.has_expect():
						self.mg.previous_phases.insert(0, w)
						# if cn.has_parent():
						# self.mg.current_node = cn.parent
					else:
						if not is_phase_nested(cn):
							sequential_phase_mem_transmission(cn, w)
							w.nesting_level += cn.nesting_level
							if self.mg.tracking:
								print("\t\t" + w.phon + " is a sequential phase, memory transmitted")												# tracking
						elif self.mg.sinking:
							w.nesting_level += cn.nesting_level
							nested_phase_mem_sinking(cn, w)
							if self.mg.tracking:
								print("\t\t" + w.phon + " is a nested phase, but sinking is allowed, then memory is transmitted")  # tracking
						else:
							w.nesting_level += cn.nesting_level + 1
						self.mg.current_node = w
				else:
					if self.mg.tracking:
						print("\t\tFAILED: word [" + w.get_expected() + " " + w.phon + "] cannot be accommodated with the current expectation")		# tracking
					self.merge_failed = True
					self.merge_failed_word = w.phon
			else:
				if self.mg.tracking:
					print("INPUT exhausted")																										# tracking
				if not len(cn.mem) > 0:
					break

		print_offline_measures(self)
		print_online_measures(self)
		print_tree(self)  																														# todo: nodes are modified/deleted during feature checking. To visualize a full tree, copies must be instantiated

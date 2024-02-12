import json

from eMG_utilities import *

# todo: implement antilocality?
# todo: implement referential buffer and binding (Schlenker Bianchi)


def is_mem_empty(node: eMG_node) -> bool:
    if len(node.mem) == 0:
        return True


def is_phase_nested(expecting_node: eMG_node) -> bool:
    if expecting_node.has_expect() or expecting_node.has_expected() is None:
        return True
    else:
        return False


def sequential_phase_mem_transmission(last_phase: eMG_node, sequential_phase: eMG_node):
    if not is_mem_empty(last_phase):
        sequential_phase.mem = last_phase.mem
        last_phase.mem = []


def nested_phase_mem_sinking(last_phase: eMG_node, sequential_phase: eMG_node):
    if not is_mem_empty(last_phase):
        sequential_phase.mem[0] = last_phase.mem.pop(0)


def remove_expect(node: eMG_node):
    return node.expect.pop(0)


def remove_expected(node: eMG_node):
    return node.expected.pop(0)


def agree(cn: eMG_node, w: eMG_node) -> bool:
    agreement = True
    agree_cn = cn.agree.split(".")
    agree_w = w.agree.split(".")
    for x in agree_cn:
        for y in agree_w:
            if (x == "1" or x == "2") and (y == "1" or y == "2"):
                if x != y:
                    print("\t\tAGREE FAILED (person): [" + cn.agree + ", " + cn.phon + "] is incompatible with [" + w.agree + ", " + w.phon + "]")  # tracking
                    set_AgreeMismatch(cn)
                    agreement = False
            if (x == "p" or x == "s") and (y == "p" or y == "s"):
                if x != y:
                    print("\t\tAGREE FAILED (number): [" + cn.agree + ", " + cn.phon + "] is incompatible with [" + w.agree + ", " + w.phon + "]")  # tracking
                    set_AgreeMismatch(cn)
                    agreement = False
            if (x == "m" or x == "f") and (y == "m" or y == "f"):
                if x != y:
                    print("\t\tAGREE FAILED (gender): [" + cn.agree + ", " + cn.phon + "] is incompatible with [" + w.agree + ", " + w.phon + "]")  # tracking
                    set_AgreeMismatch(cn)
                    agreement = False
    if agreement:
        print("\t\tAGREE OK: [" + cn.agree + ", " + cn.phon + "] is compatible with [" + w.agree + ", " + w.phon + "]")         # tracking
        if not cn.valued:
            cn.valued = True
            cn.requires_agree = False
    return agreement


def move(cn: eMG_node, w: eMG_node):
    m = copy.deepcopy(w)
    m.expect = []
    m.phon = "$t_{" + w.name + "}$"
    m.in_mem = True
    m.ref = w.name
    m.mem_index = w.index
    cn.mem.insert(0, m)


class PMG_grammar:
    root = None
    current_node = None
    step = 0
    agr_cats = []
    late_expansion = []
    late_expansion_default = False
    sinking = False
    move_failures = 0
    merge_unexpected = 0
    nesting_level = 0
    late_expansions = 0
    previous_phases = []
    n_words = 0
    words = []
    nodes = []
    word = None
    i = 0
    tracking = True

    def __init__(self, lex):
        self.lex = {}
        with open(lex) as json_file:
            self.lex = json.load(json_file)

    def merge(self, cn: eMG_node, w: eMG_node) -> str:
        if cn.has_expect():
            if w.has_expected():
                if w.is_expected(cn.get_expect()):
                    if cn.get_agree_requirement():
                        if agree(cn, w):
                            cn.agree_checked = True
                        else:
                            if self.tracking:
                                return "Agreement failure"                                                               # tracking
                    if self.tracking:
                        print("\t\tMERGE SUCCESS: [" + cn.phon + " =" + cn.get_expect() + " [" + w.get_expected() + " " + w.phon + "]]")  # tracking
                    if w.doubling:
                        choice = input(
                            "Do you want to remove [=" + cn.get_expect() + "] in '" + cn.phon + "'? [y] for 'yes remove' [n] for 'no' (choose [n] to capture post-V subject)\n")    # tracking
                        if choice == "y":
                            remove_expect(cn)
                    else:
                        remove_expect(cn)
                    remove_expected(w)
                    cn.children.append(w)
                    # cn.attach(w)                  # todo: expand this function to implement consituency-based trees (or at least Stabler's "<" ">" decorated non terminal nodes)
                    w.parent = cn
                    w.check_any_other_expectation(cn)
                    if cn.is_head_movement():
                        cn.label.pop(0)
                    if w.has_expected():
                        move(cn, w)
                        if self.tracking:
                            print("\t\tMOVE: M-buffering '" + w.phon + "' (label = " + w.name + ") phase with expected feature '" + w.get_expected() + "' in the phase '" + cn.get_label() + "'")  # tracking
                    return "OK"                                                                                      # tracking
                elif self.late_expansion_default and self.can_late_expand(cn):  # fixme: can_late_expand strongly restrict the reconstruction possibilities to cases in which 2 expected categories are present and the second comply with the incoming item; remove and simply move the item in mem to implement full reconstruction + late expansion
                    if w.is_next_expected(cn):
                        choice = input("Do you want to attempt a 'Late Expansion'? [y] for 'yes' [n] for 'no'\n")
                        if choice == "y":
                            cn.delay_expect()
                            self.merge(cn, w)
                            cn.late_expansion = True
                            self.late_expansions += 1
                            return "OK"                                                                              # tracking
                elif not w.is_in_mem():
                    cn.children.append(w)
                    w.parent = cn
                    if w.has_expected() and not w.is_in_mem():
                        if self.tracking:
                            print("\t\tMERGE: expectation '" + cn.get_expect() + "' failed: missing feature '" + w.get_expected() + "'")         # tracking
                        choice = input(
                            "No expectation satisfied. Do you want to Merge '" + w.phon + "' anyway? (this will trigger movement): [y] yes or [n] no?\n")
                        while not (choice == "y" or choice == "n"):
                            choice = input(
                                "No expectation satisfied. Do you want to Merge '" + w.phon + "' anyway? (this will trigger movement): [y] yes or [n] no? (only [y] and [n] options are available)\n")
                        if choice == "y":
                            self.merge_unexpected += 1
                            add_encoding_penalty(w)
                            if self.tracking:
                                print("encoding penalty for unexpected item assigned to " + w.phon)
                            move(cn, w)
                            if self.tracking:
                                print(
                                    "\t\tMOVE: M-buffering '" + w.phon + "' (label = " + w.name + ") phase with expected feature '" + w.get_expected() + "' in the phase '" + cn.get_label() + "'")  # tracking
                        else:
                            return "No Merge attempted."                                                             # tracking
                    return "OK"                                                                                      # tracking
                return "item unexpected and already in MEM"
            else:
                if self.tracking:
                    print("\t\tMERGE: integration failed: '" + w.phon + "' does not have features to be expected ")      # tracking
                return "nothing to be expected"                                                                      # tracking
        elif not w.has_expected():
            if w.get_label() == "RC":                                                                                # fixme: PP and RC attachment problem
                #  get_relevant_superordinate_phase()
                rc_head = copy.deepcopy(cn)
                rc_head.phon = rc_head.name
                rc_head.expected.append("D")
                cn.children.append(w)
                w.parent = cn
                w.nesting_level = cn.nesting_level + 1
                move(w, rc_head)
                if self.tracking:
                    print(
                        "\t\tMOVE: M-buffering '" + w.phon + "' (label = " + w.name + ") phase with expected feature '" + w.get_expected() + "' in the phase '" + rc_head.get_label() + "'")  # tracking
                return "OK"                                                                                          # tracking
            if w.get_label() == "AdvC" or w.get_label() == "PP":                                                                                # PP adjunct
                choice = input("Unselected phrase compatible with an adjunct interpretation. Shall I proceed considering it an adjunct? [y] yes or [n] no?\n")
                while not (choice == "y" or choice == "n"):
                    choice = input("Unselected phrase compatible with an adjunct interpretation. Shall I proceed considering it an adjunct? [y] yes or [n] no? (only [y] and [n] options are available)\n")
                if choice == "y":
                    self.merge_unexpected += 1
                    add_encoding_penalty(w)
                    cn.children.append(w)
                    w.parent = cn
                    w.nesting_level = cn.nesting_level + 1
                    return "OK"                                                                                     # tracking
                else:
                    return "No Merge attempted."
            return "MERGE: integration failed: '" + w.phon + "' cannot be selected and it is not an adjunct"        # tracking
        else:
            if self.tracking:
                print("\t\tMERGE: integration failed: '" + cn.phon + "' does not introduce any feature expectation")    # tracking
            return "no further expectations"                                                                        # tracking

    # todo: implement trie and avoid LIFO memories

    def select(self, w) -> eMG_node:  # todo: menage ambiguity by duplicating parse trees
        expect = []
        expected = []
        label = []
        ambiguous = []
        n = 0
        if w in self.lex:
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
            w_tagged = eMG_node.PMG_node(w, expect, expected, label, self.lex[w]['agree'])
            w_tagged.ambiguous = ambiguous
            if 'doubling' in self.lex[w]:
                w_tagged.doubling = True
            if 'valued' in self.lex[w]:
                w_tagged.valued = False
            if self.needs_agree(w_tagged):
                w_tagged.requires_agree = True
            w_tagged.from_lex = True
            w_tagged.index = 0
            w_tagged.outdex = 0
        else:
            if self.tracking:
                print("\t\tUnknown word '" + w + "' in the lexicon")
            w_tagged = eMG_node.PMG_node(w, expect, expected, label, "")
        return w_tagged

    def set_root(self, node: eMG_node):
        self.root = node
        self.current_node = self.root

    def set_param_agree(self, nodes: []):
        self.agr_cats = nodes

    def set_late_expansion(self, nodes: []):
        self.late_expansion = nodes

    def can_late_expand(self, node: eMG_node):
        for cat in self.late_expansion:
            if node.get_label() == cat:
                return True
        return False

    def needs_agree(self, node: eMG_node):
        if not node.agree_checked:
            for cat in self.agr_cats:
                if node.get_label() == cat:
                    return True
        return False

__author__ = 'laceyliu'
import doc_parser
import stanford_utils
import tree_parser
import sys
from nltk import Tree
mds = ["did", "do", "does", "di", "do", "doe"]
tagger = stanford_utils.new_NERtagger()
stemmer = doc_parser.stemmer
import nltk.parse

def answer_binary(q, s):
    # print q
    # print s
    q_vect = doc_parser.sent_to_vect(q.lower())
    s_vect = doc_parser.sent_to_vect(s.lower())
    # print q_vect
    # print s_vect
    for token, cnt in q_vect.items():
        if token not in s_vect and token not in mds:
            return "No."
    negs = ["not", "no", "never"]
    for neg in negs:
        if neg in q:
            return "No."
    return "Yes"

def answer_how_many(q, s):
    num = filter(str.isdigit, s)
    return num if len(num) > 0 else "0"

def answer_what(q, s):
    return ""

def answer_who(q, s):
    return ""

def answer_why(q, s):
    return ""

def answer_when(q, s):
    # handles the wh-subject-question: S -> Wh- NP VP
    q_tree = tree_parser.sent_to_tree(q)
    s_tree = tree_parser.sent_to_tree(s)
    # print s_tree
    q_np, q_vp = get_question_np_vp(q_tree)  # assume question has only one top level np, one vp.
    q_vp_head_tree = get_vp_head(q_vp)
    print "Question main verb:", tree_parser.tree_to_sent(q_vp_head_tree)
    s_vp_list = extract_vps(s_tree, match_vp_head=tree_parser.tree_to_sent(q_vp_head_tree))  # extract matching vp
    if len(s_vp_list) > 1:
        print "We got multiple VP. Chose the first one."
    ans = tree_parser.tree_to_sent(Tree('S', [q_np, extract_pp(s_vp_list[0])]))+"."
    return ans.capitalize()

def ans_when(q, sents):
    ans = ""
    for sent in sents:
        tagged = nltk.pos_tag(nltk.word_tokenize(sent[0].replace("-", " ")))
        pps = [item for item in tagged if item[1] == "IN"]
        if len(pps) == 0:
            continue
        ans = answer_when(q, sent[0])
        if len(ans) > 0:
            break
    return ans


def answer_where(q, s):
    return ""



# helper functions:
# get_np_vp: Extract top level NP, VP

def stem(word):
    return stemmer.stem(word).encode('ascii', 'ignore')

def get_question_np_vp(tree):
    np = None
    vp = None
    for subtree in tree.subtrees():
        if np is None and subtree.label() == "NP":
            np = subtree
        if vp is None and subtree.label() == "VP":
            vp = subtree
    return np, vp

def extract_vps(tree, match_vp_head=None):
    vps = []
    for subtree in tree.subtrees():
        if subtree.label() == "VP":
            if match_vp_head is not None:
                for child in subtree:
                    if child.label().startswith("VB") and stem(tree_parser.tree_to_sent(child)) == stem(match_vp_head):
                        vps += [subtree]
            else:
                vps += [subtree]
    assert(len(vps) > 0)
    return vps

def get_vp_head(vp):
    for sub in vp:
        if sub.label().startswith("VB"):
            return sub
    return None

def extract_pp(vp):
    print "Extracting PP from (", tree_parser.tree_to_sent(vp), ") ..."
    print vp
    sub_trees = []
    for sub in vp:
        if sub.label().startswith("VB"):
            sub_trees += [sub]
        elif sub.label() == "PP":  # optimize this branch.
            sub_trees += [sub]
    return Tree('VP', sub_trees)


# Yes or No questions
# print answer_binary("Do adjectives come before nouns?",
#                   "In English, adjectives come before the nouns they modify and after determiners.")
# print answer_binary("Was Harry Potter and the Prisoner of Azkaban the first film in the series to be released in both conventional and IMAX theatres?",
#                     "It was the first film in the series to be released in both conventional and IMAX theatres.")

# tests
def test():
    count = 0
    for line in open("data/question_sent_pair"):
        count += 1
        if line.startswith("When"):
            q = line.split("?")[0]
            sent = line.split("?")[1]
            print "Question:", q+"?"
            print answer_when(q, sent)
            print

test()
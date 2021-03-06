__author__ = 'laceyliu'
import stanford_utils
from nltk import Tree
parser = stanford_utils.new_parser()

def sents_to_trees(sentences):
    trees = []
    for sent in sentences:
        trees.append(parser.raw_parse(sent))
    return trees

def sent_to_tree(sentence):
    t = parser.raw_parse(sentence)
    # return t.next()
    t = parser.raw_parse(sentence)
    tree = None
    for subtree in t:
        tree = subtree
    subs = []
    for sub in tree:
        subs.append(sub)
    return Tree(tree.label(), sub)

def tree_to_sent(tree):
    if tree == None:
        return ""
    return ' '.join(tree.leaves())

def get_phrases(tree, pattern, reversed=False, sort=False):
    phrases = []
    label = tree.label()
    if tree.label() == pattern:
        phrases.append(tree)
    for t in tree.subtrees():
        if t.label() == pattern:
            phrases.append(t)
        # if pattern == "NP" and t.label() == "NNP":
        #     phrases.append(t)
    if sort == True:
        phrases = sorted(phrases, key=lambda x:len(x.leaves()), reverse=reversed)
    return phrases

def sent_to_predicate(tree):
    NP_found = False
    np, vp = "", ""
    for subtree in tree:
        if subtree.label() == "NP":
            np = tree_to_sent(subtree)
            NP_found = True
        elif subtree.label() == "VP" and NP_found:
            vp = tree_to_sent(subtree)
            break
    return (np+" "+vp).strip()

def contains_appos(tree):
    np = None
    for subtree in tree:
        if subtree.label() == "NP":
            np = subtree
            break
    if np != None and len(get_phrases(np, "NP", False, False))>2:
        return True
    return False


# Remove parts we don't want
def remove(parent, component):
    for node in parent:
        if type(node) is Tree:
            if node.label() == component:
                parent.remove(node)
            else:
                remove(node, component)

# Split sentences
def removeParts(tree):
    # remove part that tagged with "PRN"
    remove(tree, "PRN")
    # remove part that tagged with "FRAG"
    remove(tree, "FRAG")
    # tree.draw()

def seperateSBars(tree):
    NP_found = False
    np = None
    sbar_s = ""
    for sub in tree:
        if sub.label() == "NP":
            NP_found = True
            np = sub
        if NP_found and sub.label() == "SBAR":
            WHNP_found = False
            sbar = None
            for sub_bar in sub:
                if sub_bar.label() == "WHNP":
                    WHNP_found = True
                    sbar = sub.copy(deep=True)
                    remove(tree, "SBAR")
                    remove(sbar, "WHNP")
                    break
            if WHNP_found:
                for sub_bar in sub:
                    if sub_bar.label() != "WHNP":
                        sbar_s += " ".join([l for l in sub_bar.leaves()])
                sbar.insert(0, np)
                #sbar_s = " ".join([l for l in np.leaves()])+sbar_s
                break

    return filter(sbar, None)

def remove_appos(tree):
    np = None
    vp = ""
    NP_found = False
    if contains_appos(tree):
        for subtree in tree:
            if subtree.label() == "NP":
                np = subtree
                NP_found = True
            elif subtree.label() == "VP" and NP_found:
                vp = tree_to_sent(subtree)
                break
        sub_nps = get_phrases(np, "NP", True, True)
        sub_nps.pop(0)
        sent = tree_to_sent(sub_nps[0])+" "+vp
    return sent

tests =['Starbucks is doing very well lately.',
               'Overall, while it may seem there is already a Starbucks on every corner, Starbucks still has a lot of room to grow.',
               'They just began expansion into food products, which has been going quite well so far for them.',
               'I can attest that my own expenditure when going to Starbucks has increased, in lieu of these food products.',
               'Starbucks is also indeed expanding their number of stores as well.',
               'Starbucks still sees strong sales growth here in the united states, and intends to actually continue increasing this.',
               'Starbucks also has one of the more successful loyalty programs, which accounts for 30%  of all transactions being loyalty-program-based.',
               'As if news could not get any more positive for the company, Brazilian weather has become ideal for producing coffee beans.',
               'Brazil is the world\'s #1 coffee producer, the source of about 1/3rd of the entire world\'s supply!',
               'Given the dry weather, coffee farmers have amped up production, to take as much of an advantage as possible with the dry weather.',
               'Increase in supply... well you know the rules...',]
# preds = []
# for sent in tests:
#     tree = sent_to_tree(sent)
#     if contains_appos(tree):
#         preds += appps_to_sents(tree)
#     else:
#         pred = sent_to_predicate(tree)
#         preds.append(pred)
# for pred in preds:
#     print pred
# def pre_process_sentence(input_sentence):
#     simple_predicate_check = False
#     apposition_check = False
#     relative_clause_check = False
#     good_sentences = []
#     final_sentences = []
#
#     #english_parser = StanfordParser("stanford-parser.jar", "stanford-parser-3.4.1-models.jar")
#     english_parser = stanford_utils.new_parser()
#     sentences = english_parser.raw_parse(input_sentence)
#
#     #check if sentence is in the form S -> NP VP .
#     for t in sentences:
#         for tr in t:
#             tr1 = str(tr)
#             s1 = Tree.fromstring(tr1)
#             s2 = s1.productions()
#
#     #Turn sentences into NP VP format
#     found_NP = False
#     while found_NP == False:
#         if s1[0].label() == '.' or s1[0].label() == ':':
#             found_NP = True
#         elif s1[0].label() != 'NP':
#             #print s1[0].label()
#             s1.pop(0)
#         else:
#             found_NP = True
#
#
#     if s1.label() == 'S' and s1[0].label() == 'NP' and s1[1].label() == 'VP' and s1[2].label() == '.':
#         simple_predicate_check = True
#         #print "TRUE"
#
#     #Split sentences into NP VP
#     np_found = False
#     np_start = ''
#     vp_start = ''
#     vp_repeated = False
#     vp_re_counter = 0
#     vp_re_list = []
#     for i in s1.subtrees():
#         #Process NP
#         if (i.label() == 'NP' and len(i.leaves()) < 4 and np_found == False and simple_predicate_check == True):
#             temp_list2 = i.leaves()
#             for f in temp_list2:
#                 if np_start == '':
#                     np_start = np_start + f
#                 elif np_start != '':
#                     np_start = np_start + ' ' + f
#             np_found = True
#
#         #Proccess VP
#         if (i.label() == 'VP' and vp_repeated == False and simple_predicate_check == True):
#             temp_list = i.leaves()
#             for y in xrange(min(len(vp_re_list), len(temp_list))):
#                 if len(vp_re_list) > 0 and (temp_list[y] in vp_re_list):
#                     vp_re_counter += 1
#             if (vp_re_counter < 3):
#                 for u in temp_list:
#                     if(vp_start == ''):
#                         vp_start = vp_start + u
#                     elif(vp_start != ''):
#                         vp_start = vp_start + ' ' + u
#                 vp_start = np_start + ' ' + vp_start
#                 good_sentences.append(vp_start)
#                 #print good_sentences
#                 vp_start = ''
#                 for h in xrange(len(temp_list)):
#                     vp_re_list.append(temp_list[h])
#             elif(vp_re_counter >= 3):
#                 vp_repeated = True
#     return good_sentences
#
# def get_final_sentences(input_sentence_list):
#     output = []
#     for i in input_sentence_list:
#         temp_list = pre_process_sentence(i)
#         for sentence in temp_list:
#             if (sentence[-1] != '.'):
#                 sentence = sentence + '.'
#             if (sentence[0].isupper() != True):
#                 sentence = ' '.join(word[0].upper() + word[1:] for word in sentence.split())
#             print "Original:    "+i
#             print "Processed:   "+sentence
#             print
#             output.append(sentence)
#     return output
#
#
# def pre_process_sentence(input_sentence):
#     simple_predicate_check = False
#     apposition_check = False
#     relative_clause_check = False
#     good_sentences = []
#     final_sentences = []
#
#     #english_parser = StanfordParser("stanford-parser.jar", "stanford-parser-3.4.1-models.jar")
#     english_parser = stanford_utils.new_parser()
#     sentences = english_parser.raw_parse(input_sentence)
#
#     #check if sentence is in the form S -> NP VP .
#     for t in sentences:
#         for tr in t:
#             tr1 = str(tr)
#             s1 = Tree.fromstring(tr1)
#             s2 = s1.productions()
#
#     #Turn sentences into NP VP format
#     found_NP = False
#     while found_NP == False:
#         if s1[0].label() == '.' or s1[0].label() == ':':
#             found_NP = True
#         elif s1[0].label() != 'NP':
#             #print s1[0].label()
#             s1.pop(0)
#         else:
#             found_NP = True
#
#
#     if s1.label() == 'S' and s1[0].label() == 'NP' and s1[1].label() == 'VP' and s1[2].label() == '.':
#         simple_predicate_check = True
#         #print "TRUE"
#
#     #Split sentences into NP VP
#     np_found = False
#     np_start = ''
#     vp_start = ''
#     vp_repeated = False
#     vp_re_counter = 0
#     vp_re_list = []
#     for i in s1.subtrees():
#         #Process NP
#         if (i.label() == 'NP' and len(i.leaves()) < 4 and np_found == False and simple_predicate_check == True):
#             temp_list2 = i.leaves()
#             for f in temp_list2:
#                 if np_start == '':
#                     np_start = np_start + f
#                 elif np_start != '':
#                     np_start = np_start + ' ' + f
#             np_found = True
#
#         #Proccess VP
#         if (i.label() == 'VP' and vp_repeated == False and simple_predicate_check == True):
#             temp_list = i.leaves()
#             for y in xrange(min(len(vp_re_list), len(temp_list))):
#                 if len(vp_re_list) > 0 and (temp_list[y] in vp_re_list):
#                     vp_re_counter += 1
#             if (vp_re_counter < 3):
#                 for u in temp_list:
#                     if(vp_start == ''):
#                         vp_start = vp_start + u
#                     elif(vp_start != ''):
#                         vp_start = vp_start + ' ' + u
#                 vp_start = np_start + ' ' + vp_start
#                 good_sentences.append(vp_start)
#                 #print good_sentences
#                 vp_start = ''
#                 for h in xrange(len(temp_list)):
#                     vp_re_list.append(temp_list[h])
#             elif(vp_re_counter >= 3):
#                 vp_repeated = True
#     return good_sentences
#
# def get_final_sentences(input_sentence_list):
#     output = []
#     for i in input_sentence_list:
#         temp_list = pre_process_sentence(i)
#         for sentence in temp_list:
#             if (sentence[-1] != '.'):
#                 sentence = sentence + '.'
#             if (sentence[0].isupper() != True):
#                 sentence = ' '.join(word[0].upper() + word[1:] for word in sentence.split())
#             print "Original:    "+i
#             print "Processed:   "+sentence
#             print
#             output.append(sentence)
#     return output
#

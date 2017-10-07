from node import Node
import math
from copy import *
import parse
import random


def split_on_attr(examples, attribute):
    # input an array of dict in which each dict is a tuple
    # output a dict ot lists in which keys are values of attribute and list are a bunch of tuples
    # this function is to split data into different groups based on the value
    # of a specific attribute
    result = {}
    for data in examples:
        value = data[attribute]
        if value not in result:  # if this value does not exist in dictionary
            result[value] = [data]  # create a new list for this value
        else:
            result[value].append(data)  # append the data to the already existing list
    return result
# ======== Test case =============================
'''
examples, attr = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=1, b=2, Class=0), dict(a=1, b=3, Class=1)], 'Class'
output = split_on_attr(examples, attr)
print(output)
for i in output:
    data = output[i]
    print(data)
    for j in data:
        print(j)
        for k in j:
            print(j[k])
'''


def mode(examples, attribute):
    # calculate the majority class
    value_freq = {}  # frequency of each value
    values = []  # list of values
    most_freq = 0  # the most frequent class
    mode = None
    for tuples in examples:
        value = tuples[attribute]
        values.append(value)
        if value not in value_freq:
            value_freq[value] = 1
    for key in value_freq:
        if values.count(key) > most_freq and not key == '?':
            most_freq = values.count(key)
            mode = key
    return mode
 #======== Test case =============================
#examples = [dict(a=1, b=0, Class='?'), dict(a=1, b=1, Class='?'), dict(a=1, b=2, Class='?'), dict(a=1, b=3, Class=1)]
# print mode(examples, 'Class')


def entropy(data):
    attr = {}
    total = 0
    entropy = 0
    for i in data:
        if not(i.get('Class') in attr):
            attr[i.get('Class')] = 1
        else:
            attr[i.get('Class')] += 1
        total = total + 1
    # print(attr)
    for i in attr:
        entropy = entropy - (float(attr.get(i)) / total) * math.log(float(attr.get(i)) / total, 2)

    # print(entropy)
    return entropy


def choose_best_attr(data):
    attrlist = []
    for i in data:
        for j in i:
            if(j != 'Class' and not(j in attrlist)):
                attrlist.append(j)
    # print(attrlist)
    total = 0
    subentropy = {}
    subset = {}
    entropy = {}

    for i in attrlist:
        children = []
        for j in data:
            for k in j:
                #---------------------------------------------change-----------------
                if(k == i and not(j.get(i) in children) and not(j.get(i) == '?')):
                    children.append(j.get(i))
        # print(children)

        for l in children:
            for j in data:
                if (j.get(i) == l):
                    # if(not(j.get(i) in subentropy)):
                    #---------------------------------#
                    subentropy.setdefault(j.get(i), {})
                    if(not(j.get('Class') in subentropy[j.get(i)])):
                        subentropy[j.get(i)][j.get('Class')] = 1
                    else:
                        subentropy[j.get(i)][j.get('Class')] = subentropy[
                            j.get(i)][j.get('Class')] + 1
                    #----------------------------------#
                    if(not(j.get(i) in subset)):
                        subset[j.get(i)] = 1
                    else:
                        subset[j.get(i)] = subset[j.get(i)] + 1

        # print(subset)
        # print(subentropy)
        for j in subset:
            total = total + subset[j]
        for j in subset:
            for k in subentropy.get(j):
                if(not(i in entropy)):
                    entropy[i] = -float(subentropy[j][k]) / subset[j] * \
                        math.log(float(subentropy[j][k]) / subset[j], 2) * float(subset[j]) / total
                else:
                    entropy[i] = entropy[i] - float(subentropy[j][k]) / subset[j] * math.log(
                        float(subentropy[j][k]) / subset[j], 2) * float(subset[j]) / total
            # entropy[i]=entropy[i]*float(subset[j])/total
#        for j in subentropy:
#            if(j in entropy)
        subset.clear()
        subentropy.clear()
        total = 0
    # print(entropy)
    k = ''
    minimum = 2
    for i in entropy:
        if(entropy[i] < minimum):
            minimum = entropy[i]
            k = i
    # print(k)
    return k


def isAttributeSame(origin_data):
    data = deepcopy(origin_data)
    for i in data:
        i.pop('Class')
    for i in data:
        if not (cmp(data[0], i) == 0):
            return False
    return True


def ID3(examples, default):

    node = Node()  # new node
    # best attribute to split on
    best_attribute = choose_best_attr(examples)
    values = []  # record values of this attribute
    examples_copy = deepcopy(examples)
    # base case:
    # 1. entropy == 0; 2. reach the depth; 3. only one tuple
    if examples == {}:
        node.label = default
        return node
    if entropy(examples) == 0 or isAttributeSame(examples_copy):
        node.label = mode(examples, 'Class')
        return node

    # returns a dictionary with best_attribute'values as keys

    # fill missing data
    # we have to do this because if we simply drop the tuples with '?' of best_attribute
    # then we will lose these data forever.
    mode_attr = mode(examples, best_attribute)
    for a_tuple in examples_copy:
        if a_tuple[best_attribute] == '?':
            a_tuple[best_attribute] = mode_attr

    attrkeydata = split_on_attr(examples, best_attribute)

    # add a children for each nominal attribute
    for key in attrkeydata:
        node.children[key] = ID3(attrkeydata[key], mode(examples, 'Class'))
        values.append(key)

    node.decision_attribute = best_attribute
    node.values = values
    # print node, depth
    # print node.children, entropy(examples)
    return node


def modeinprune(data_set):
    value_freq = {}  # tracks frequency of each value
    most_frequent = 0  # tracks the most frequent number
    mode = None
    for data in data_set:
        value = data[0]
        if value not in value_freq:
            value_freq[value] = 1
        else:
            value_freq[value] += 1
    for key, frequency in value_freq.iteritems():
        if frequency > most_frequent:
            most_frequent = frequency
            mode = key
    return mode


def prune(root, examples):
    stack = []
    stack.append(root)
    num_pruned = 0
    while stack:
        old_acc = test(root, examples)
        node = stack.pop(0)
        subtree_nodes = [node]
        node_cpy = deepcopy(node)
        labels = []
        while subtree_nodes:
            tree_node = subtree_nodes.pop(0)
            if tree_node.label is not None:
                labels.append([tree_node.label])
            else:
                for k, v in tree_node.children.items():
                    subtree_nodes.append(v)
        label = modeinprune(labels)
        old_label = deepcopy(node.label)
        old_children = deepcopy(node.children)
        old_decision_attribute = deepcopy(node.decision_attribute)
        old_value = deepcopy(node.values)
        node.label = label
        node.children = None
        node.decision_attribute = None
        node.values = None
        new_acc = test(root, examples)
        if new_acc > old_acc:
            num_pruned += 1
        else:
            node.label = old_label
            node.children = old_children
            node.decision_attribute = old_decision_attribute
            node.values = old_value
        if node.children is not None:
            for k, v in node.children.items():
                stack.append(v)
    if num_pruned > 0:
        prune(root, examples)


def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''
    total = 0
    count = 0
    for a_tuple in examples:
        result = evaluate(node, a_tuple)
        if result == a_tuple['Class']:
            count += 1
        total += 1
    return (float)(count) / (float)(total)


def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    if not (node.label == None):
            # print node.label
        return node.label
    attribute = node.decision_attribute
    for i in example:
        # print i
        if i == attribute:
            if example[i] == '?':# if value is missing then we randomly choose a child
               example[i] = random.sample(node.values, 1)[0]
            for j in node.children:
                if j == example[i]:
                    return evaluate(node.children[j], example)

#===========test case===========================

data = parse.parse('house_votes_84.data')
# random.shuffle(data1)
validation = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1),
              dict(a=0, b=0, Class=1), dict(a=0, b=0, Class=0)]
tree = ID3(data, 'democrat')
# tree.printTreeRecurse(tree)
# print test(tree, data)
# tree.printTree()
#prune(tree, validation)
# tree.printTree()
# node.printTree()
#a = evaluate(tree, dict(a=3, b=0))
#prune(tree, data)
# tree.printTreeRecurse(tree)


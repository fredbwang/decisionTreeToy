import ID3, parse
def printTreeRecurse(self, depth = 0): # DFS print
    node = [self]
    if node:
        if node[0].label is not None:
            print depth * ".." + "Class:" + (str)(node[0].label)
        else:
            print depth * ".." + node[0].decision_attribute + ":" + (str)(node[0].values)
    if node[0].children is not None:
        children = node[0].children
        for child in children:
            printTreeRecurse(children[child],depth + 1)

data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=0, b=1, Class=0), dict(a=0, b=0, Class=1),
        dict(a=2, b=0, Class=2), dict(a=2, b=1, Class=2), dict(a=2, b=1, Class=2), dict(a=2, b=0, Class=3),
        dict(a=4, b=0, Class=4), dict(a=2, b=4, Class=6), dict(a=4, b=2, Class=4), dict(a=4, b=0, Class=6)]
tree = ID3.ID3(data, 0)
#printTreeRecurse(tree)
data = parse.parse('house_votes_84.data')
subdata = ID3.split_on_attr(data, 'handicapped-infants')
print subdata
tree = ID3.ID3(data, 0)
#tree.printTreeRecurse(tree)


class Node:
    def __init__(self):
        self.label = None
        self.children = {}
        self.decision_attribute = None
        self.name = None
        self.values = [] # store the values of decision_attribute
	# you may want to add additional fields here...

    def getLabel(self):
        return self.label

    def getChildren(self):
        return self.children

    def getAttribute(self):
        return self.decision_attribute

    def clearChildren(self):
        self.children = {}

    def printTree(self): # BFS print
        thislevel = [self]
        depth = 30
        while thislevel:
            nextlevel = []
            print " "*depth,
            for n in thislevel:
                if n.label is not None:
                    print "Class:" + (str)(n.label),
                else:
                    print n.decision_attribute + ":" + (str)(n.values), # prints decision attribute
                    for key in n.children:
                        nextlevel.append(n.children[key])
            print #feed line
            depth -= len(self.values)*2
            thislevel = nextlevel

    def printTreeRecurse(self, self_local, depth = 0): # DFS print
    #need to add a self local to
        node = [self_local]
        if node:
            if node[0].label is not None:
                print depth * ".." + "Class:" + (str)(node[0].label)
            else:
                print depth * ".." + node[0].decision_attribute + ":" + (str)(node[0].values)
        if node[0].children is not None:
            children = node[0].children
            for child in children:
                self.printTreeRecurse(children[child], depth + 1)


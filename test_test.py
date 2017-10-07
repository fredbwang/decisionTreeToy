import ID3

data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=0, b=1, Class=0), dict(a=0, b=0, Class=1),
        dict(a=2, b=0, Class=2), dict(a=2, b=1, Class=2), dict(a=2, b=1, Class=2), dict(a=2, b=0, Class=3),
        dict(a=4, b=0, Class=4), dict(a=2, b=4, Class=6), dict(a=4, b=2, Class=4), dict(a=4, b=0, Class=6)]

tree = ID3.ID3(data, 0)
ID3.printTreeRecurse(tree)

examples = [dict(a=4, b=1, Class=4), dict(a=2, b=4, Class=6), dict(a=4, b=2, Class=4)]
acc = ID3.test(tree, examples)
print acc

def prune(node, examples):
    '''
    Takes in a trained tree and a validation set of examples.  Prunes nodes in order
    to improve accuracy on the validation data; the precise pruning strategy is up to you.
    '''
    node_local = [node]
    queue={}
    Classifer={}
    for i in node_local[0].children:
        if not node_local[0].children[i].label == None:
            queue[i]=node.children[i]
    if len(queue)==0:
        for i in node_local[0].children:
            if not node_local[0].children[i].label in Classifer:
                Classifer[node_local[0].children[i].label]=1
            else:
                Classifer[node_local[0].children[i].label]=Classifer[node_local[0].children[i].label]+1
        newnode=Node()
        globalmax=0
        myClass=0
        for i in Classifer:
            if Classifer>globalmax:
                myClass=i

        newnode.lable=myClass
        newnode.childern=None
        newnode.decision_attribute=None
        newnode.name=None

        if test(node,examples)>test(newnode,examples):
            node_local[0]=newnode
        else:
            return
    newqueue = deepcopy(queue)
    while not len(queue)==0:
        for i in newqueue:
            subdata = split_on_attr(examples, node_local[0].decision_attribute)
            prune(newqueue[i], subdata[i])
            queue.pop(i)

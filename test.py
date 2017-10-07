import ID3


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

data = [dict(a=1, b=0, Class=1),
        dict(a=1, b=1, Class=1),
        dict(a=0, b=1, Class=0),
        dict(a=0, b=0, Class=1)]
valid = [dict(a=1, b=0, Class=1),
         dict(a=1, b=1, Class=1),
         dict(a=0, b=0, Class=0),
         dict(a=0, b=0, Class=0)]
attr = 'a'
# print split_on_attr(data, attr)

tree = ID3.ID3(data, 0)
tree.printTree()
ID3.prune(tree, valid)
tree.printTree()
data = [1,2,3,4,5]
print data[2:6]
example = dict(a='?', b=0)
print ID3.evaluate(tree, example)

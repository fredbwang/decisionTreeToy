
def split_on_attr(data_set, attribute):
#input an array of dict in which each dict is a tuple
#output a dict ot lists in which keys are values of attribute and list are a bunch of tuples
#this function is to split data into different groups based on the value of a specific attribute
    result = {}
    for data in data_set:
        value = data[attribute]
        if value not in result: # if this value does not exist in dictionary
            result[value] = [data] # create a new list for this value
        else:
            result[value].append(data) # append the data to the already existing list
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

def ID3(data_set, default):

    node = Node()  # new node
    # best attribute to split on
    best_attribute = pick_best_attribute(data_set)

    #base case:
    #1. entropy == 0; 2. reach the depth; 3. only one tuple
    if entropy(data_set) == 0 or depth >= len(data_set[0]) or len(data_set) == 1:
        node.label = mode(data_set)
        return node

    # returns a dictionary with best_attribute'values as keys
    attrkeydata = split_on_attr(data_set, best_attribute)
    '''
    ### filling in missing data ###
    for key in attrkeydata.keys():
        if key is None:
            # find most common attribute and add the missing attribute data into the
            # most common attribute
            greatest_length = -1
            mode_attr = None
        for attr, data in attrkeydata.iteritems():
            if len(data) > greatest_length:
                    greatest_length = len(data)
                    mode_attr = attr
            for data in attrkeydata[key]:
                # adds all the None data into the mode attribute
                attrkeydata[mode_attr].append(data)
            attrkeydata.pop(key, None)  # removes the None attribute data
    '''
    # add a children for each nominal attribute
    for key in attrkeydata:
        node.children[key] = ID3(attrkeydata[key], default)
    node.decision_attribute = best_attribute
    # print node.children
    return node

def mode(examples):

    value_freq = {} # tracks frequency of each value
    most_freq = 0; # tracks the most frequent number
    mode = None
    for tuples in examples:
        value = tuples['Class']
        if value not in value_freq:
            value_freq[value] = 1
        else:
            value_freq[value] += 1
    for key in value_freq:
        if  value_freq[key] > most_freq:
            most_freq = value_freq[key]
            mode = key
    return mode
 #======== Test case =============================
# data_set = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=1, b=2, Class=1), dict(a=1, b=3, Class=1)]
# print(mode(data_set))
def mode1(examples):
#calculate the majority class
    value_freq = {} # frequency of each value
    values = [] # list of values
    most_freq = 0; # the most frequent class
    mode = None
    for tuples in examples:
        value = tuples['Class']
        values.append(value)
        if value not in value_freq:
            value_freq[value] = 1
    for key in value_freq:
        if  values.count(key) > most_freq:
            most_freq = values.count(key)
            mode = key
    return mode
#======== Test case =============================
data_set = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=1, b=2, Class=1), dict(a=1, b=3, Class=1)]
print(mode1(data_set))

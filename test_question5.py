import matplotlib.pyplot as plt
import numpy as np
import ID3
import parse
import random

datapct = []
data = parse.parse('house_votes_84.data')
for i in range(10, 30):
    datapct.append(i)

#randomsize suppose to be 100
def getAccWithOutPrune(data, randomSize):
    acc = []
    for scale in range(10, 30):# warning: this will take a long time
        total = []
        for i in range(randomSize):
            random.shuffle(data)

            train = data[:scale/2]
            valid = data[scale/2: scale]
            #test = data[3 * len(data) / 4:]
            test = data[scale:]

            tree = ID3.ID3(train + valid, 0)
            acc_test = ID3.test(tree, test)
            total.append(acc_test)

        acc.append(sum(total) / randomSize)
    return acc

def getAccWithPrune(data, randomSize):
    acc = []
    for scale in range(10, 30):# warning: this will take a long time
        total = []
        for i in range(randomSize):
            random.shuffle(data)

            train = data[:scale/2]
            valid = data[scale/2: scale]
            #test = data[3 * len(data) / 4:]
            test = data[scale:]

            tree = ID3.ID3(train, 0)
            ID3.prune(tree, valid)

            acc_test = ID3.test(tree, test)
            total.append(acc_test)

        acc.append(sum(total) / randomSize)
    return acc

#accp = getAccWithPrune(data, 100)
#print accp
acc = getAccWithOutPrune(data, 100)
#print acc
#plt.plot(datapct, acc)
#plt.plot(datapct, accp)
'''
diff = []
for i in range(len(acc)):
    diff.append(accp[i] - acc[i])
'''
plt.plot(datapct, acc)
plt.xlabel('number of training examples')
plt.ylabel('Accuracy on test data')
#plt.ylim(0.75, 0.97)
plt.show()


import random
import sys
import string
import math
import array
import itertools
import operator
import collections
from collections import Counter
from ete3 import PhyloTree

# struct node to make the desicion tree
class node:
    def __init__(self,col=-1,value=None,results=None,accepted=None,rejected=None):
        self.col=col
        self.value=value
        self.results=results
        self.accepted=accepted
        self.rejected=rejected

# read the dataset
def reading():
    inputs = [];
    for line in sys.stdin:
        result = line.split(',');
        inputs.append(result);
    return inputs

# Get the probability of one value in a specific column
def P_Column(count,total):
    return float(count)/float(total);

# Get the number of equals values in a row
def getEquals(data):
    counts={}
    for x in data:
        v=x[len(x)-1]
        if v not in counts:
            counts[v]=0
        counts[v]+=1
    return counts

# Divides a dataset on by a specific column by function to detect values that are equal to the given value
def split(data,index,value):
    split_function=lambda row:row[index]==value
    dataset1=[row for row in data if split_function(row)]
    dataset2=[row for row in data if not split_function(row)]
    return (dataset1,dataset2)

# Get the entropy by the count of each value in the row
def H(data):
    entropy=0
    values=getEquals(data)
    for x in values.keys():
        p=float(values[x])/len(data)
        entropy-=p*math.log(p,2)
    return entropy

#Count the number of attributes in the row less the objective value.
def getAttributes_Column(data):
    count=len(data[0])-1
    return count

# Execution of the id3 algorithm and creating the desicion tree
def ID3(data,root):
    best_IG=0.0
    best_criteria=None
    best_datasets=None
    column_values={}
    
    if len(data) == 0:
        return node()
    
    H_general = H(data)
    column_without_objective= getAttributes_Column(data)

    for column_index in range(0,column_without_objective):
        # check visited with key as the value given by the index and value = 42
        for x in data:
            column_values[x[column_index]]=42

        # check the values of the dataset and make the split with the IG of each new dataset
        for value in column_values.keys():
            (dataset1,dataset2)=split(data,column_index,value)
            # Get the probabilities
            p = P_Column(len(dataset1),len(data))
            p_ = 1-p
            # Get the IG given the datasets chossed by the value
            IG = H_general-p*H(dataset1)-p_*H(dataset2)
            # Get the greates IG of all the data set
            if IG>best_IG and len(dataset1)>0 and len(dataset2)>0:
                best_IG = IG
                best_criteria = (column_index,value)
                best_datasets = (dataset1,dataset2)
    
    # Check if the IG can be splited; if best_IG > 0 the dataset can continue to be splited in other case it stoped becouse it is pure
    if best_IG>0:
        # node to print the tree
        A =root.add_child(name = value)
        # Recursive call with the accepted value path and rejected value path
        accepted=ID3(best_datasets[0],A)
        not_accepted=ID3(best_datasets[1],A)
        # return a node with the values in the actual iteration
        return node(col=best_criteria[0],value=best_criteria[1],accepted=accepted,rejected=not_accepted)
    else:
        # returns result values of the leafs
        return node(results=getEquals(data))

# Classify the new information
def Classifier(data,desiciontree):
    if desiciontree.results!=None:
        return desiciontree.results
    else:
        # check the value with the index of the column in the branch if it is accepted or rejected
        v=data[desiciontree.col]
        path = None
        if v == desiciontree.value:
            path = desiciontree.accepted
        else:
            path = desiciontree.rejected
        return Classifier(data, path)

def main():
    input_data = reading()
    new_data = []
    root = PhyloTree()
    tree = ID3(input_data,root)
    print root
    # file = open("verifyData.txt", "r+")
    with open("verifyData.txt") as f:
        for line in f:
            result = line.split(',');
            new_data.append(result)

    for data in new_data:
        print Classifier(data,tree)

if __name__ == "__main__":
    main()
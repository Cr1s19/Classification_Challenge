import random
import sys
import string
import math
import array
import itertools

def reading():
    inputs = [];
    last_input = [];
    for line in sys.stdin:
        result = line.split(',');
        inputs.append(result);
    # for i in inputs[0]:
    #     print i, '\n'
    return inputs

# Get the values of one column in specific index
def getColumn(list,index):
    column = [];
    for x in list:
        column.append(x[index])
    return column

# Get the number of equals values in a column
def getEquals(list, string, index):
    v = getColumn(list,index)
    count = 0
    for x in v:
        if x == string:
            count +=1
    return count

# Get numbers of differents types in a column given the entire list with an especific index
def getDifferents(list,index):
    v = getColumn(list,index)
    types = []
    for x in v:
        if types.count(x) >= 1:
            continue
        else:
            types.append(x)
    return types

# Get the values that are repeated in the column given by the index
def getDifferents_Column(column):
    types = []
    for x in column:
        if types.count(x) >= 1:
            continue
        else:
            types.append(x)
    return types

#Get the total number of data
def getTotal(list):
    count = 0
    for x in list:
        count += 1
    return count;

# Get the probability of one value
def P(list,string,total,index):
    count = getEquals(list,string,index)
    return float(count)/float(total);

# Make pairs for the first column and the second column given by the indexes
def makePairs(list,index,indexSecond):
    column1 = getColumn(list,index)
    column2 = getColumn(list,indexSecond)
    values_dict = []
    for x,y in zip(column1,column2):
        value = {x,y}
        values_dict.append(value);
    return values_dict

def comapareColumns(list,index,indexSecond):
    count = 0
    getDifferents(list,index);
    values_dict = makePairs(list,index,indexSecond)
    v = getDifferents_Column(values_dict)
    for x in v:
        print x


# Get the General Entropy
def H(list,total,index):
    strings_total = getDifferents(list,index)
    sumatory = 0
    for x in strings_total:
        p = P(list,x,total,index)
        sumatory -= p*math.log(p,2)
    return sumatory

# Get the entropy by value in a specific index
def HI(list,total,index,indexSecond):
    strings_total = getDifferents(list,index)
    total_iterations = strings_total[-1]
    sumatory = 0
    for x in strings_total[0]:
        print ""
    return sumatory



def main():
    input_data = reading()
    t = getTotal(input_data)
    H(input_data,t,-1)
    comapareColumns(input_data,0,-1)


 
if __name__ == "__main__":
    main()
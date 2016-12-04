import random
import sys
import string
import math
import array
import itertools
import operator

def reading():
    inputs = [];
    last_input = [];
    for line in sys.stdin:
        result = line.split(',');
        inputs.append(result);
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

# Get equals in a specific columns compairing pairs
def getEquals_Column(list,pair):
    count = 0
    for x in list:
        if x == pair:
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

# Get the total of columns in the data set
def getTotal_Column(list):
    count = 0
    for x in list:
        for y in x:
            count += 1
        break
    return count

# Get the probability of one value
def P(list,string,total,index):
    count = getEquals(list,string,index)
    return float(count)/float(total);

# Get the probability of one value in a specific column comapared by pairs
def P_Column(count,total):
    return float(count)/float(total);

# Make pairs for the first column and the second column given by the indexes
def makePairs(list,index,indexSecond):
    column1 = getColumn(list,index)
    column2 = getColumn(list,indexSecond)
    values_dict = []
    for x,y in zip(column1,column2):
        value = {x:y}
        values_dict.append(value);
    return values_dict

# Get the General Entropy
def H(list,total,index):
    strings_total = getDifferents(list,index)
    sumatory = 0
    for x in strings_total:
        p = P(list,x,total,index)
        sumatory -= p*math.log(p,2)
    return sumatory

# Get the Entropy of the sum in the values of acolumn compared by another column given by indexes
def HI(list,total,index,indexSecond):
    getDifferents(list,index);
    values_dict = makePairs(list,index,indexSecond)
    v = getDifferents_Column(values_dict)
    p = 0
    count = 0
    p_total = 0
    sub_total = 0
    sumatory = 0
    for x in v:
        count = getEquals_Column(values_dict,x)
        sub_total = getEquals(list,x.keys()[0],index)
        p = P_Column(count,sub_total)
        p_total = P(list,x.keys()[0],total,index)
        sumatory -= p_total*(p*math.log(p,2))
    return sumatory

# Get the information gain of the indexes given
def IG(list,total,index,indexSecond):
    h = H(list,total,indexSecond)
    hi = HI(list,total,index,indexSecond)
    result = h-hi
    return result

# Get the greatest information gain
def getGratestIG(list):
    if not list:
        return 0
    else:
        return max(list)

# Sort the data set given the IG
def SortIG(list,index):
    for x in list:
        value = sorted(list,key=operator.itemgetter(index));
    return value

# Split the dataSet given the IG
def SplitIG(list,value,index):
    data = SortIG(list,index)
    splittables = []

    for x in data:
        if x[index] == value:
            splittables.append(x)
    return splittables

def SplitIG_1(list,values,index):
    dataSet = []
    for x in values:
        sig = SplitIG(list,x,index)
        dataSet.append(sig)
    return dataSet

def SplitIG_without_index(list,value,index):
    data = []
    for x in list:
        for y in x:
            if  y[index] == value:
                y.pop(index)
                data.append(y)
    print data
    return data



def checkEquals(iterator):
   return len(set(iterator)) <= 1

def id3(list,total):
    total_horizontal = getTotal_Column(list)
    total_vertical = getTotal(list)
    values = []
    ig = 0
    split = 0
    DataSet = []
    Data = []
    newDataSet = []

    for x in xrange(0,total_horizontal-1):
        ig = IG(list,total_vertical,x,-1)
        values.append(ig)

    ggi = getGratestIG(values)
    for i,x in enumerate(values):
        if x == ggi:
            split = i

    values = getDifferents(list,split)
    DataSet = SplitIG_1(list,values,split)

    for x in values:
        sig_i = SplitIG_without_index(DataSet,x,split)
        newDataSet.append(sig_i)

def main():
    input_data = reading()
    t = getTotal(input_data)
    H(input_data,t,-1)
    id3(input_data,t)


 
if __name__ == "__main__":
    main()
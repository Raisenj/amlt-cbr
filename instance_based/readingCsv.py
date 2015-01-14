#!/usr/bin/python
#################################################################
import csv
from Attributes import RealAttr, CategoricalAttr
from Case import Case


def readCase(row, types, names, label_name):
    attrs = {}
    for i in xrange(0, len(types)):
        if types[i] == 'r':
            attrs[names[i]] = RealAttr(row[i])
        elif types[i] == 'c':
            attrs[names[i]] = CategoricalAttr(row[i])
        else:
            return (False,'wrong item on csv file')

    #attrs contains the attributes of the case
    label = attrs[label_name]
    attrs.pop(label_name)
    return (True, Case(attrs, {label_name : label}))

def readCasesFromCsv(filename, types, names, label_name):
    cases = []
    m = len(types)
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != m:
                return (False,'the elements of the csv are not '\
                        'consistent with the structure provided.')
            result = readCase(row, types, names, label_name)
            if result[0] == False:
                return result
            else:
                cases.append(result[1])
    return (True, cases)



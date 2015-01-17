#!/usr/bin/python
#################################################################
import csv
from Attributes import RealAttr, CategoricalAttr
from Case import Case

def readCurrentCase(row, types, names):
    attrs = {}
    for i in xrange(0, len(types)):
        if types[i] == 'r':
            attrs[names[i]] = RealAttr(row[i])
        elif types[i] == 'c':
            attrs[names[i]] = CategoricalAttr(row[i])
        else:
            raise Exception('wrong item on input')

    #attrs contains the attributes of the case
    return Case(attrs)

def readCase(row, types, names, label_name):
    attrs = {}
    for i in xrange(0, len(types)):
        if types[i] == 'r':
            attrs[names[i]] = RealAttr(row[i])
        elif types[i] == 'c':
            attrs[names[i]] = CategoricalAttr(row[i])
        else:
            raise Exception('wrong item on input')

    #attrs contains the attributes of the case
    label = attrs[label_name]
    attrs.pop(label_name)
    return Case(attrs, {label_name : label})

def readCasesFromCsv(filename, types, names, label_name):
    cases = []
    m = len(types)
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                if len(row) != m:
                    raise Exception('the elements of the csv are not '\
                            'consistent with the structure provided.')
                case = readCase(row, types, names, label_name)
                cases.append(case)
    return cases


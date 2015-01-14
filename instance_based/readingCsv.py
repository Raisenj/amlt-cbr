#!/usr/bin/python
#################################################################
import csv
from Attributes import RealAttr, CategoricalAttr
from Case import Case


def readCase(row, types, names, solution):
    attrs = {}
    for i in range (0,len(types)):
        if types[i] == 'r':
            a = RealAttr(row[i])
            attrs[names[i]] = a
        elif types[i] == 'c':
            c = CategoricalAttr(row[i])
            attrs[names[i]] = c
        else:
            return (False,'wrong item on csv file')
    '''attrs contains the attributes of the case'''
    solution_attr_name = names[solution-1]
    c = Case(attrs,solution_attr_name)
    return (True, c)
    


def readCasesFromCsv(filename, types, names, solution):
    cases = []
    n = len(types)
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != n:
                return (False,'the elements of the csv are not '\
                        'consistent with the structure provided.')
            result = readCase(row, types, names, solution)
            if result[0] == False:
                return result
            else:
                cases.append(result[1])
    return (True, cases)
                        


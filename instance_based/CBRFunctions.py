#!/usr/bin/python
import os
import numpy as np
from functools import partial
from operator import itemgetter

def checkFilename(filename):
    abspath = os.path.abspath(filename)
    if not os.path.isfile(abspath):
        return (False,'the filename does not exists')
    if not filename.endswith('csv'):
        return (False,'the file is not a csv file')
    return (True, abspath)

def readKindOfAttrs():
    variables_input = raw_input(
                'Introduce the kind of variables: ')
    variables = variables_input.split(',')
    n = len(variables)
    variables_types = []
    for i in range(0,n):
        if not str(variables[i]).strip() in ['r','c']:
            return (False, 'wrong input')
        variables_types.append(str(variables[i]).strip())
    return (True, variables_types)

def readAttrNames(n):
    variables_input = raw_input(
                'Introduce the names of the variables: ')
    variables = variables_input.split(',')
    if len(variables) != n:
        return (False,'The number of variables is inconsistent')
    variables_names = []
    for i in range(0,n):
        variables_names.append(str(variables[i]).strip())

    if len(set(variables_names)) != len(variables_names):
        return (False, 'The attribute names must be uniques')
    return (True,variables_names)

def readSolutionVariable(n):
    variables_input = raw_input(
            'Introduce the variable that is the solution (number): ')
    solution = int(variables_input)
    if solution > n or solution < 1:
        return (False, 'Wrong Number')
    else:
        return (True,solution)

def normalize(v,maximum_v,minimum_v):
    return (v-minimum_v)/(maximum_v-minimum_v)

def adapt(similar_cases):
    labels = list(set([c.labelValue() for (c,s) in similar_cases]))
    labels_punct = {}
    exactMatch = None
    for l in labels:
        labels_punct[l] = 0
    for (c,s) in similar_cases:
        if c.evaluation == True:
            if s == 0:
                exactMatch = (True,c.labelValue())
                return
            else:
                labels_punct[c.labelValue()] += (100/(s*s) + c.utility)
        else: 
            if s == 0:
                exactMatch = (False, c.labelValue())
            labels_punct[c.labelValue()] -= (100/(s*s) + c.utility)
    if exactMatch!= None:
        if exactMatch[0]:
            solution = exactMatch[1]
        else:
            labels_punct.pop(exactMatch[1])
    solution = max(labels_punct.iteritems(), key=itemgetter(1))[0]
    return solution
        






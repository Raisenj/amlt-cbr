#!/usr/bin/python
import os
import numpy as np
import random
from functools import partial
from operator import itemgetter

def checkFilename(filename):
    abspath = os.path.abspath(filename)
    if not os.path.isfile(abspath):
        raise Exception('the filename does not exists')
    if not filename.endswith('csv'):
        raise Exception('the file is not a csv file')
    return abspath

def readKindOfAttrs():
    variables_input = raw_input(
                'Introduce the kind of variables: ')
    variables = variables_input.split(',')
    n = len(variables)
    variables_types = []
    for i in xrange(0, n):
        if not str(variables[i]).strip() in ['r','c']:
            raise Exception('wrong input')
        variables_types.append(str(variables[i]).strip())
    return variables_types

def readAttrNames(n):
    variables_input = raw_input(
                'Introduce the names of the variables: ')
    variables = variables_input.split(',')
    if len(variables) != n:
        raise Exception('The number of variables is inconsistent')

    variables_names = []
    for i in xrange(0, n):
        variables_names.append(str(variables[i]).strip())

    if len(set(variables_names)) != len(variables_names):
        raise Exception('The attribute names must be uniques')
    return variables_names

def readSolutionVariable(n):
    variables_input = raw_input(
            'Introduce the variable that is the solution (number): ')
    solution = int(variables_input)

    if solution > n or solution < 1:
        raise Exception('Wrong Number')

    return solution

def normalize(v, maximum_v, minimum_v):
    return (v - minimum_v)/(maximum_v - minimum_v)

def adapt(similar_cases, labels):
    new_labels = list(labels) 
    labels = list(set([c.labelValue() for (c,s) in similar_cases]))
    labels_punct = {}
    exactMatch = None
    for l in labels:
        labels_punct[l] = 0
    for (c,s) in similar_cases:
        if c.evaluation == True:
            if s == 0:
                exactMatch = (True,c.labelValue())
                return c.labelValue()
            else:
                labels_punct[c.labelValue()] += (100/(s*s) + c.utility)
        else:
            if s == 0:
                exactMatch = (False, c.labelValue())
            else:
                labels_punct[c.labelValue()] -= (100/(s*s) + c.utility)
    if exactMatch!= None:
        if exactMatch[0]:
            solution = exactMatch[1]
        else:
            labels_punct.pop(exactMatch[1])
            if not labels_punct:
                print 'new_labels:'
                print new_labels
                print 'exactMatch:'
                print exactMatch
                new_labels.remove(exactMatch[1])
                solution = new_labels[random.randint(0,len(new_labels)-1)]
                return solution
    solution = min(labels_punct.iteritems(), key=itemgetter(1))[0]
    return solution

def evaluate(label_solution, cases_retrieved):
    input = 'Introduce the real solution:'
    real_solution = raw_input(input)
    if label_solution.lower() == real_solution.lower():
        for c in cases_retrieved:
            c.utility += 1 
        return True
    else:
        for c in cases_retrieved:
            c.utility -= 1 
        return False

def retain(case):
    return True

#!/usr/bin/python
import os
import numpy as np
from functools import partial

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
    for i in xrange(0,n):
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

def normalize(values):
    for v in l:
        print v
    maximum = np.max(l)
    minimum = np.min(l)
    mapFunc = partial(normEquation,minimum = minimum, maximum = maximum)
    l = map(mapFunc,l)
    return l

def normEquation(v,minimum,maximum):
    return (v - minimum)/(maximum-minimum)

def weightedSum(l):
    sum_ = 0
    for v in l:
        sum_+=v
    return sum_/len(l)


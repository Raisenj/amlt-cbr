#!/usr/bin/python
import os

def checkFilename(filename):
    abspath = os.path.abspath(filename)
    if not os.path.isfile(abspath):
        return (False,'the filename does not exists')
    if not filename.endswith('csv'):
        return (False,'the file is not a csv file')
    return (True, abspath)

def readKindOfAttrs():
    variables_input = raw_input(
                'Introduce the kind of variables:')
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
                'Introduce the names of the variables:')
    variables = variables_input.split(',')
    if len(variables) != n:
        return (False,'The number of variables is inconsistent')
    variables_names = []
    for i in range(0,n):
        variables_names.append(str(variables[i]).strip())
    return (True,variables_names)

def readSolutionVariable(n):
    variables_input = raw_input(
            'Introduce the variable that is the solution (number):')
    solution = int(variables_input)
    if solution > n or solution < 1:
        return (False, 'Wrong Number')
    else:
        return (True,solution)





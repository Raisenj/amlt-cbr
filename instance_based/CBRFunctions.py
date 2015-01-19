#!/usr/bin/python
import os
import numpy as np
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
                break
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

def stringSim(s1, s2):
    """
    Calculates Jarow-Winkler string similiarity, returns
    a similarity value between 0 and 1
    """
    def jarow(s1,s2): 
        """  
        Returns a number between 1 and 0, where 1 is the most similar 
        example: print jarow("martha","marhta") 
        """ 
        m= jarow_m(s1,s2) 
        t1 = jarow_t(s1,s2) 
        t2 = jarow_t(s2,s1) 
        if t1 and t2 and m != 0: #Avoid division by zero
            t = float(t1)/float(t2) 
            d = 0.1 
            # This is the Jaro distance 
            d_j = 1.0/3.0 * ((m/len(s1)) + (m/len(s2)) + ((m - t)/float(m))) 
            # If the strings are prefixed similar, they get more weight 
            l = winkler_l(s1,s2) 
            return d_j + (l * 0.1 * (1 - d_j))   
        else:
            if t1 == 0 and t2 == 0: 
            # Similarity between two empty strings = 1
                if s1 == '' and s2 == '':
                    return 1    
        return 0

    def winkler_l(s1,s2): 
        """ 
        Number of matches between the four first characters 
        """ 
        firstCharMatch = 0 
        counter = 0 
        for s_j,s_i in zip(s1,s2): 
            if s_j == s_i: 
                firstCharMatch += 1 
            counter += 1 
            if counter > 4: 
                break 
        return firstCharMatch
 
    def jarow_m(s1,s2): 
        """ 
        Number of total matching characters 
        """ 
        matchingChars = 0 
        d = {} 
        for s in s1: 
            d[s] = True 
        for s in s2: 
            if d.has_key(s): 
                matchingChars += 1 
        return matchingChars
    
    def jarow_t(s1,s2): 
        """ 
        Number of transpositions 
        """ 
        t= 0 
        pos = {} 
        counter = 0 
        for s in s1: 
            pos[s] = counter 
        counter += 1 
        counter = 0 
        for s in s2: 
            if pos.has_key(s): 
                if pos[s] != counter: 
                    t += 1 
            counter += 1 
        return t 
        
        

# FIXME: Miguel function pasted
#def retain(solution_case, solution_label, kcase, csvpath):
#    """
#    Retain process. At the moment working with only ONE case match
#    """
#    # 0.0 similarity means the case presented to he cbr is already in its DB and
#    # we will not enter retain process.
#   
#    print '\nWelcome to Retain Phase'
#    newDataRow = []
#    match = False
#    for k in solution_case.attributes.keys():
#        newDataRow.append(str(solution_case.attributes[k].askValue()))
#    newDataRow.append(solution_label)  # Put the solution case in csv style to check vs whole dataset.csv
#        
#    print 'This was the new case: '+ str(newDataRow)
#    with open(csvpath, 'rb') as csvfile:
#        reader = csv.reader(csvfile)
#        for line in reader:
#            if newDataRow[0:4] == line[0:4]:
#                # Check if the cbr has given the correct label
#                match = True
#                break
#                    
#        if match == True and newDataRow[-1] == line[-1]:
#                        
#            print "\nThe expert says: The CBR did a good job, this case corresponds to this label"
#            kcase.utility += 1
#            kcase.printCase()     
#            ## OPTIONAL: Add the solution_case to the database of cases.
#        else:
#            print '\nThe expert says: The CBR did not match this values to the correct class'   
#            ## OPTIONAL: Reduce utility of retrieved case  

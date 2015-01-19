#/usr/bin/python
from flatMemory import flatMemory
from CBRFunctions import *
from Case import Case
from Attributes import RealAttr, CategoricalAttr, StringAttr

def buildTTCases(memory,datasets, ratio):
    num_cases = int(ratio * float(memory.num_cases))
    num_cases_cat = num_cases/len(datasets.keys())
    cases = []
    test_cases = []
    for k in datasets.keys():
        for c in [datasets[k][i] 
                for i in range(0,num_cases_cat)]:
            cases.append(c)
        for c in [datasets[k][i] 
                for i in range(num_cases_cat,
                    len(datasets[k]))]:
            test_cases.append(c)
    return (cases, test_cases)

def test1(memory, datasets):
    print 'test 1 (ratio 8/10):'
    ratio = float(8./10.)
    (cases,test_cases) = buildTTCases(memory, datasets,ratio)
    print 'len cases: ', len(cases)
    print 'len test_cases: ', len(test_cases)
    memory = flatMemory(cases)
    settings = {}
    settings['k'] = 5
    executeCBR(memory, test_cases,settings)

def test2(memory, datasets):
    print 'test 2 (ratio 9/10):'
    ratio = float(9./10.)
    (cases,test_cases) = buildTTCases(memory, datasets,ratio)
    print 'len cases: ', len(cases)
    print 'len test_cases: ', len(test_cases)
    memory = flatMemory(cases)
    settings = {}
    settings['k'] = 5
    executeCBR(memory, test_cases,settings)

def test3():
    print 'test 3:'
def test4():
    print 'test 4:'
def test5():
    print 'test 5:'

def executeCBR(memory,test_cases,settings=None):
    trues = 0
    falses = 0
    attrType = test_cases[0].label.values()[0].attrType()
    for c in test_cases:
        label = c.label.copy()
        cases = memory.retrieve(c, settings['k'])
        sol_label = adapt(cases, memory.solutions)
        result = evaluateA(sol_label, 
                label.values()[0].askValue(),
                [c for (c,s) in cases])
        if result:
            trues+=1
        else:
            falses+=1
        if retain(c):
            if attrType == 'r':
                if not result:
                    case = Case(c.attributes, 
                        { label.keys()[0] : 
                            RealAttr(sol_label)},False)
                else:
                    case = Case(c.attributes, 
                        { label.keys()[0] : 
                            RealAttr(sol_label)})
            elif attrType == 'c':
                if not result:
                    case = Case(c.attributes, 
                        { label.keys()[0] : 
                            CategoricalAttr(sol_label)},False)
                else:
                    case = Case(c.attributes, 
                        { label.keys()[0] : 
                            CategoricalAttr(sol_label)},False)

            elif attrType == 's':
                if not result:
                    case = Case(c.attributes, 
                        { label.keys()[0] : 
                            StringAttr(sol_label)},False)
                else:
                    case = Case(c.attributes, 
                        { label.keys()[0] : 
                            StringAttr(sol_label)},False)
            memory.retain(case)
    print 'trues: ', trues
    print 'falses: ', falses


        

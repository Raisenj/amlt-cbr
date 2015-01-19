#!/usr/bin/python
from Console import Console
from readingCsv import readCasesFromCsv, readCurrentCase
from CBRFunctions import *
from CBRTests import *
from kdTree import kdTree
from flatMemory import flatMemory
from Case import Case
from Attributes import RealAttr, CategoricalAttr, StringAttr
import os
import sys

class CBR(Console):

    def __init__(self):
        intro = '\nCBR tool\n'
        print intro
        Console.__init__(self)

        self.cases_flat = None
        self.cases_hierarchical = None
        self.memory = None
        self.solution = None
        self.label_name = None
        self.current_case = None
        self.K = 1

    def do_loadCasesFromCsv(self, args):
        """Loads the cases from the specified csv file. Example:
            loadCasesFromCsv <filename>"""

        try:
            params = args.split()
            if len(params) != 1:
                raise Exception('wrong number of arguments')
    
            abspath = checkFilename(params[0])
    
            info = 'We need to know the kind of attributes present '\
                        'in the csv file.\nIntroduce such types of '\
                        'variables. Example:\n\tr,r,s,c\n'\
                        'In this case the csv file will have 4 columns, '\
                        'being the two first real values, the third a string and the last one'\
                        ' a categorical one.'
            print '\n',info
            types = readKindOfAttrs()
    
            n = len(types)
            # At this point we know how many colums have the csv and the
            # kind of variables.
            info = 'Now we need to know the names of such variables '\
                        'and which one is the solution. Example\n\t'\
                        'sepal_l, sepal_w, petal_l, iris_class, 4'
            names = readAttrNames(n)
    
            info = 'Now we need to know which parameter specifies the '\
                        'solution of the case. Indicate that through a '\
                        'number'
            print '\n',info
            self.solution = readSolutionVariable(n)
            self.label_name = names[self.solution - 1]
    
            cases = readCasesFromCsv(abspath, types, names, self.label_name)
    
            self.cases_flat = flatMemory(cases)
            self.cases_hierarchical = kdTree(cases)
            self.memory = self.cases_flat

        except Exception as error:
            print error

    def do_printMemory(self, args):
        """Prints the cases stored in memory"""
        try:
            if self.memory:
                self.memory.printMemory()
            else:
                print 'No loaded cases'
        except Exception as error:
            print error

    def do_printCurrentCase(self, args):
        """Prints the current case"""
        try:
            if self.current_case:
                self.current_case.printCase()
            else:
                print 'There is no current case loaded'
        except Exception as error:
            print error

    def do_newCase(self, args):
        """Introduce a new case to be analyzed"""
        try:
            if not self.memory:
                raise Exception('First you need to load the library of cases')

            case0 = self.cases_flat.cases[0]
            names = case0.attrNames()
            attributes = {}
            for n in names:
                intro = 'Introduce '+n+':\n'
                v = raw_input(intro)
                t = case0.attributes[n].attrType()
                if t == 'r':
                    attributes[n]= RealAttr(v)
                if t == 'c':
                    attributes[n]= CategoricalAttr(v)
                if t == 's':
                    attributes[n] = StringAttr(v)

            self.current_case = Case(attributes)
        except Exception as error:
            print error

    def do_setRetrieveParameter(self, args):
        """Set the K parameter for the retrieve phase"""
        try:
            params = args.split()
            if len(params) != 1:
                raise Exception('wrong number of arguments')

            self.K = int(params[0])
        except Exception as error:
            print error

    def do_setMemoryModel(self, args):
        """Set the memory model: flat or hierarchical"""
        try:
            params = args.split()
            if len(params) != 1:
                raise Exception('wrong number of arguments')

            if params[0].lower() == "flat":
                self.memory = self.cases_flat
            elif params[0].lower() == "hierarchical":
                self.memory = self.cases_hierarchical
            else:
                raise Exception('invalid option')

        except Exception as error:
            print error

    def do_setWeights(self, args):
        """Introduce the weights for each attribute"""
        try:
            if not self.memory:
                raise Exception('First you need to load the library of cases')

            names = self.cases_flat.cases[0].attrNames()
            weights = {}
            for n in names:
                intro = 'Introduce ' + n + ':\n'
                weights[n] = float(raw_input(intro))

            Case.weights = weights

        except Exception as error:
            print error

    def do_executeCBR(self, args):
        """Run CBR"""
        try:
            cases = self.memory.retrieve(self.current_case, self.K)
            """ cases = [(case,similarity)] cases is a list of case similarity
            tuples."""
            
            #cases2 = self.cases_hierarchical.retrieve(self.current_case, self.K)

            print 'Those cases are:'
            for (c,s) in cases:
                c.printCase()
                print 'sim: ', s

            sol_label = adapt(cases, self.memory.solutions)
            print 'ADAPTATION - Result (Solution):'
            print sol_label

            result = evaluate(sol_label,[c for (c,s) in cases])

            print 'Result: ',result
            if not result:
                self.current_case.evaluation = False
            
            example_case = self.cases_flat.cases[0]
            attrType = example_case.label.values()[0].attrType()
            
            if retain(self.current_case):
                if attrType == 'r':
                    if not result:
                        case = Case(self.current_case.attributes, 
                            { self.cases_flat.cases[0].label.keys()[0] : 
                                RealAttr(sol_label)},False)
                    else:
                        case = Case(self.current_case.attributes, 
                            { self.cases_flat.cases[0].label.keys()[0] : 
                                RealAttr(sol_label)})

                elif attrType == 'c':
                    if not result:
                        case = Case(self.current_case.attributes, 
                            { self.cases_flat.cases[0].label.keys()[0] : 
                                CategoricalAttr(sol_label)},False)
                    else:
                        case = Case(self.current_case.attributes, 
                            { self.cases_flat.cases[0].label.keys()[0] : 
                                CategoricalAttr(sol_label)})

                elif attrType == 's':
                    if not result:
                        case = Case(self.current_case.attributes, 
                            { self.cases_flat.cases[0].label.keys()[0] : 
                                StringAttr(sol_label)},False)
                    else:
                        case = Case(self.current_case.attributes, 
                            { self.cases_flat.cases[0].label.keys()[0] : 
                                StringAttr(sol_label)})
                self.memory.retain(case)
        except Exception as error:
            print error
    
    def do_testDataSet(self,args):
        
        case_example = self.cases_flat.cases[0]
        types = self.memory.solutions
        dataset = {}
        for t in types:
            dataset[t] = self.memory.getCases(t)

        test1(self.memory, dataset)
        test2(self.memory, dataset)
        test3()
        test4()
        test5()

    
        

if __name__ == "__main__":
    cbr = CBR()
    cbr.cmdloop()


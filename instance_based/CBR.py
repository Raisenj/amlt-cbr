#!/usr/bin/python
from Console import Console
from readingCsv import readCasesFromCsv, readCurrentCase
from CBRFunctions import *
from kdTree import kdTree
from flatMemory import flatMemory
from Case import Case
from Attributes import RealAttr, CategoricalAttr
import os
import sys
from operator import itemgetter

class CBR(Console):

    def __init__(self):
        intro = '\nCBR tool\n'
        print intro
        Console.__init__(self)

        self.cases_flat = None
        self.cases_hierarchical = None
        self.solution = None
        self.label_name = None
        self.current_case = None

    def do_loadCasesFromCsv(self, args):
        """Loads the cases from the specified csv file. Example:
            loadCasesFromCsv <filename>"""

        try:
            params = args.split()
            if len(params) != 1:
                raise Exception('wrong numbe of arguments')

            abspath = checkFilename(params[0])

            info = 'We need to know the kind of attributes present '\
                    'in the csv file.\nIntroduce such types of '\
                    'variables. Example:\n\tr,r,r,c\n'\
                    'In this case the csv file will have 4 columns, '\
                    'being the three first real values and the last one'\
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
            #self.cases_hierarchical = kdTree(self.cases_flat)
        except Exception as error:
            print error

    def do_printFlatMemory(self, args):
        """Prints the cases stored at flat memory"""
        try:
            if self.cases_flat:
                self.cases_flat.printFlatMemory()
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

    def do_newCase(self,args):
        """Introduce a new case to be analyzed"""
        try:
            if not self.cases_flat:
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

            self.current_case = Case(attributes)
        except Exception as error:
            print error

    def do_executeCBR(self,args):
        try:
            similarities = self.cases_flat.retrieve(self.current_case)
            similarities = zip(range(0, len(similarities)), similarities)
            similarities.sort(key = itemgetter(1))

            print 'RETRIEVE - Results:'
            print 'The nearest 5 cases are:'
            print similarities[:5]

            cases = [(self.cases_flat.cases[index], similarity)
                    for (index, similarity) in similarities[:5]]

            print 'Those cases are:'
            for (c, s) in cases:
                c.printCase()
                print 'sim: ', s

            solution = adapt(cases)

            print 'ADAPTATION - Result (Solution):'
            print solution
        except Exception as error:
            print error

if __name__ == "__main__":
    cbr = CBR()
    cbr.cmdloop()


#!/usr/bin/python
from Console import Console
from readingCsv import readCasesFromCsv, readCurrentCase
from CBRFunctions import *
from kdTree import kdTree
from flatMemory import flatMemory
import os
import sys

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
        """Loads the cases from the specified csv file"""

        try:
            params = args.split()
            if len(params) != 1:
                raise Exception('wrong numbe of arguments')

            filename = params[0]
            abspath = checkFilename(filename)

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
            intro = 'Introduce a new case following the format of the '\
                    'previous loaded cases:\n'
            if not self.cases_flat:
                raise Exception('First you need to load the library of cases')

            user_input = raw_input(intro)
            input_values = user_input.split(',')
            if len(input_values) != self.cases_flat.num_dim:
                raise Exception('wrong input')

            self.current_case = readCurrentCase(input_values,
                    self.cases_flat.cases[0].types(),
                    self.cases_flat.cases[0].names())
        except Exception as error:
            print error

    def do_executeCBR(self,args):
        self.cases_flat.retrieve(self.current_case)


if __name__ == "__main__":
    cbr = CBR()
    cbr.cmdloop()


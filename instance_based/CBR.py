#!/usr/bin/python
from Console import Console
from readingCsv import readCasesFromCsv, readCurrentCase
from CBRFunctions import *
from kdTree import kdTree
from flatMemory import flatMemory
from Case import Case
from Attributes import RealAttr, CategoricalAttr
import os
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

        params = args.split()
        if len(params) != 1:
            print 'wrong parameters'
            return

        filename = params[0]
        result = checkFilename(filename)
        if result[0] == False:
            print result[1]
            return
        abspath = result[1]

        info = 'We need to know the kind of attributes present '\
                'in the csv file.\nIntroduce such types of '\
                'variables. Example:\n\tr,r,r,c\n'\
                'In this case the csv file will have 4 columns, '\
                'being the three first real values and the last one'\
                ' a categorical one.'
        print '\n',info
        result = readKindOfAttrs()
        if result[0] == False:
            print result[1]
            return
        types = result[1]

        n = len(types)

        # At this point we know how many colums have the csv and the
        # kind of variables.
        info = 'Now we need to know the names of such variables '\
                'and which one is the solution. Example\n\t'\
                'sepal_l, sepal_w, petal_l, iris_class, 4'
        result = readAttrNames(n)
        if result[0] == False:
            print result[1]
            return
        names = result[1]

        info = 'Now we need to know which parameter specifies the '\
                'solution of the case. Indicate that through a '\
                'number'
        print '\n',info
        result = readSolutionVariable(n)
        if result[0] == False:
            print result[1]
            return
        self.solution = result[1]
        self.label_name = names[result[1]-1]

        result = readCasesFromCsv(abspath, types, names, self.label_name)
        if result[0] == False:
            print result[1]
            return

        self.cases_flat = flatMemory(result[1])
        #self.cases_hierarchical = kdTree(self.cases_flat)

    
    def do_printFlatMemory(self, args):
        """Prints the cases stored at flat memory"""
        if self.cases_flat:
            self.cases_flat.printFlatMemory()
        else:
            print 'No loaded cases'

    def do_printCurrentCase(self, args):
        """Prints the current case"""
        if self.current_case:
            self.current_case.printCase()
        else:
            print 'There is no current case loaded'

    def do_newCase(self,args):
        """Introduce a new case to be analyzed"""
        if not self.cases_flat:
            print 'First you need to load the library of cases'
            return
        
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

    def do_executeCBR(self,args):
        similarities = self.cases_flat.retrieve(self.current_case)
        similarities = zip(xrange(0,len(similarities)), similarities)
        sorted_similarities =sorted(similarities, key=itemgetter(1))

        print 'RETRIEVE - Results:'
        print 'The nearest 5 cases are:'
        sim = [i for i in sorted_similarities[:5]]
        print sim
        cases = [case for case in 
                [self.cases_flat.cases[index] for (index,similarity) in sim]]
        cases_similar = zip(cases,[s[1] for s in sim])
        print 'Those cases are:'
        for c in cases:
            c.printCase()
        print 'Those cases are:'
        for c in cases_similar:
            c[0].printCase()
            print 'sim: ', c[1]
        solution = adapt(cases_similar)

        print 'ADAPTATION - Result (Solution):'
        print solution



if __name__ == "__main__":
    cbr = CBR()
    cbr.cmdloop()


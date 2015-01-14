#!/usr/bin/python
from Console import Console
from readingCsv import readCasesFromCsv
from CBRFunctions import *
import os
#################################################################
class CBR(Console):

    _cases = None

    def __init__(self):
        intro = '\nCBR tool\n'
        print '\n',intro
        Console.__init__(self)
        
    def do_loadCasesFromCsv(self,args):
        """Loads the cases from the specified csv file"""
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
        solution = result[1]

        result = readCasesFromCsv(abspath,types,names,solution)
        if result[0] == False:
            print result[1]
            return
        _cases = result[1]
        print '\nCases Loaded.\nCASES:'
        for c in _cases:
            c.printCase()
        
    

if __name__ == "__main__":
    cbr = CBR()
    cbr.cmdloop()


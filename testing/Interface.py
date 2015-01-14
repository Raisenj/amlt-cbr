__all__ = ['Interface']

from Console import Console
import os
import cPickle as pickle
from Case import Case
from Matcher import Matcher

class Interface(Console):
    def __init__(self):
        print 'Interface init'
        Console.__init__(self)
    
    def do_loadCaseLibrary(self, arg):
        """
        Loads the case library.
        Use:
            loadCaseLibrary <filename>      Filename must be a pickle file
        """
        filename = arg
        if os.path.isfile(filename):
            if filename.endswith('.pickle'):
                with open(filename, "rb") as fp:
                    self.cases = pickle.load(fp)

                self.matcher = Matcher(self.cases)
                print '%d loaded cases' % len(self.cases)
            else:
                print 'Filename must be a pickle file'
        else:
            print 'Filename does not exists'

    def do_loadCase(self, arg):
        """
        Load a case to classify.

        loadCase                            Show loaded case
        loadCase manual <SL> <SW> <PL> <PW>    Load a case manually specifying the 4 values of a case
        loadCase automatic <file>           Load a case from a file
        """

        if arg in '':
            print 'Current Load Case:'
            try:
                self.load_case
            except AttributeError:
                print 'No case was loaded'
            else:
                print self.load_case
        elif len(arg) > 1:
            if 'manual' in arg:
                params = arg.split(' ')[1:]
                if len(params) == 4:
                    item = {
                            'SepalLength':params[0],
                            'SepalWidth':params[1],
                            'PetalLength':params[2],
                            'PetalWidth':params[3],
                            'IrisClass': 'null'
                            }
                    self.load_case = Case(item)
                else:
                    print 'Unrecognized Parameters'
                    Console.do_help(self, 'loadCase')

        else:
            print 'Unrecognized Parameters'
            Console.do_help(self, 'loadCase')

    def do_printCases(self, arg):
        """
        Print the cases loaded to the Case Library
        """
        try:
           self.cases
        except AttributeError:
            print 'No cases on Case Library'
        else:
            for c in self.cases:
                print c
            print '%d printed cases' % len(self.cases)

    def do_classify(self, arg):
        """
        Classifies the current loaded case
        """
        try:
            self.load_case
        except AttributeError:
            print 'No case was loaded'
        else:
            print 'Current loaded case: ', self.load_case
            try:
                self.matcher
            except AttributeError:
                print 'No matcher was loaded'
            else:
                result = self.matcher.match(self.load_case,1)
                print 'result: '
                for r in result:
                    print r
                    print '\n'

if __name__ == "__main__":
    interface = Interface()
    interface.cmdloop()

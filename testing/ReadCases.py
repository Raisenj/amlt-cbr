#!/usr/bin/python

import cPickle as pickle
import Case
import Attributes

def readPickle(filename):
    f = open(filename,'r')
    cases = pickle.load(f)
    for c in cases:
        print c
    return len(cases)

def main():
    try:
        import sys
        if len(sys.argv) < 2:
            print "Usage: %s <filename>." % sys.argv[0]
            sys.exit(1)
        else:
            filename = sys.argv[1]

        if filename.endswith(".pickle"):
            ncases = readPickle(filename)
        else:
            print "Usage: %s <filename>. <filename> must be a pickle" % sys.argv[0]
            sys.exit(1)
        print "Parsed %d items" % ncases 

    except RuntimeError, e:
        sys.stderr.write("Fatal error occurred: %s\n" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()


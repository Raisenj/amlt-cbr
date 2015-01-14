#!/usr/bin/python

import cPickle as pickle
import csv
import os

def parse_csv(filename):
    with open(filename, "rb") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        return parse_items(reader)

def parse_items(lines):
    items = []
    for line in lines:
        if not line:
            continue
        else:
            items.append(parse_item(line))
    return items

def parse_item(line):
    item = {}
    item['SepalLength']=float(line[0].strip())
    item['SepalWidth']=float(line[1].strip())
    item['PetalLength']=float(line[2].strip())
    item['PetalWidth']=float(line[3].strip())
    item['IrisClass']=line[4].strip()
    return item


def main():
    try:
        import sys
        if len(sys.argv) < 2:
            print "Usage: %s <filename>." % sys.argv[0]
            sys.exit(1)
        else:
            filename = sys.argv[1]

        if filename.endswith(".csv"):
            items = parse_csv(filename)
        else:
            print "Usage: %s <filename>. <filename> must be a csv" % sys.argv[0]
            sys.exit(1)
        print "Parsed %d items" % len(items)


        ranges={}
        sl = [float(i['SepalLength']) for i in items if 'SepalLength' in i]
        ranges['SepalLength'] = (min(sl), max(sl))
        sw = [float(i['SepalWidth']) for i in items if 'SepalWidth' in i]
        ranges['SepalWidth'] = (min(sw), max(sw))
        pl = [float(i['PetalLength']) for i in items if 'PetalLength' in i]
        ranges['PetalLength'] = (min(pl), max(pl))
        pw = [float(i['PetalWidth']) for i in items if 'PetalWidth' in i]
        ranges['PetalWidth'] = (min(pw), max(pw))
        iris_classes = list(set([c['IrisClass'] for c in items if 'IrisClass' in c]))
        print 'Ranges sl: ', ranges['SepalLength']
        print 'Ranges sw: ', ranges['SepalWidth'] 
        print 'Ranges pl: ', ranges['PetalLength']
        print 'Ranges pw: ', ranges['PetalWidth']
        print 'IrisClass:',iris_classes
       
        filename_out = os.path.dirname(filename)+'/'+filename.split(
                os.path.dirname(filename)+'/')[1].split('.csv')[0]+'.pickle'

        if os.path.exists(filename_out):
            print "Case storage file %s exists. Not creating cases." % filename_out
        else:
            print "Creating and storing Case objects in %s:" % filename_out
            from Case import Case
            cases = []
            for i,item in enumerate(items):
                print i, item
                cases.append(Case(item))
                if (i+1)%100 == 0:
                    print "  %d cases created..." % (i+1)
            print "  Storing cases...",
            with open(filename_out, "wb") as fp:
                pickle.dump((cases), fp, -1)
                print "done."

    except RuntimeError, e:
        sys.stderr.write("Fatal error occurred: %s\n" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()

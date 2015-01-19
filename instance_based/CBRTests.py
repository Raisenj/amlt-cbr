#/usr/bin/python
from flatMemory import flatMemory

def test1(memory, datasets):
    print 'test 1:'
    ratio = float(8./10.)
    print 'ratio: ', ratio
    print 'cases: ', memory.num_cases
    num_cases = int(ratio * float(memory.num_cases))
    print 'ncases: ', num_cases

    num_cases_cat = num_cases/len(datasets.keys())
    print 'numcases cat: ', num_cases_cat
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
    print 'lcses:', len(cases)
    print 'lcsesT:', len(test_cases)
    

    memory = flatMemory(cases)

def test2():
    print 'test 2:'
def test3():
    print 'test 3:'
def test4():
    print 'test 4:'
def test5():
    print 'test 5:'


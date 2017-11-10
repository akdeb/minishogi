import os, sys, difflib
from mini_shogi import *

def main():
    #tfpath = os.path.join('testcmd.txt')
    #testf = open(tfpath, 'w')
    # count=1
    for file in os.listdir('tests'):
        if file.endswith('.in'):
            # print('{}. Test: {}\nCorrect: \nNotes: \n\n'.format(count, os.path.splitext(file)[0]),file=testf)
            #print('python3 mini_shogi.py -f tests/{}.in | diff -u tests/{}.out -'.format(os.path.splitext(file)[0], os.path.splitext(file)[0]),file=testf)
            path = os.path.join('sols/',os.path.splitext(file)[0] + '.txt')
            orig_stdout = sys.stdout
            f = open(path, 'w')
            sys.stdout = f
            fileMode(os.path.join('tests/',file))
            sys.stdout = orig_stdout
            f.close()
            diff = difflib.ndiff(open(path).readlines(), open('tests/'+os.path.splitext(file)[0] + '.out').readlines())
            # find a way to compare the 2 files you have
            #print(''.join(diff))
            # count+=1
    #testf.close()

if __name__ == '__main__':
    main()

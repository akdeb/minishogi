'''
Filename: inputMain.py

Function:
This script handles inputs and parses the input and calls the appropriate function
Possible flags:
1. -i
2. -f <input filename> | diff -u <comparison output filename> -
3. nothing
4. else
'''

import sys
import utils as utils
from main import intMode, fileMode

if __name__ == '__main__':
    flag = sys.argv[1]
    if flag == '-i':
        intMode()
    elif flag == '-f':
        fileMode()
    else:
        print('Please enter a correct flag!')

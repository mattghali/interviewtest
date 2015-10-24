#!/usr/bin/env python

'''
    This script accepts an arbitrary list of file paths on the command
    line, then returns a random single line of text from one randomly
    selected file via stdout.
'''

import random, sys

# Initialize random number generator
random.seed()

# build a list of files
filelist = sys.argv[1:]

# Choose a random file to read from
filename = random.choice(filelist)

with open(filename, 'r') as fh:

    # Count lines in the file
    linecount = sum(1 for line in fh.readlines())

    # Seek back to beginning of file
    fh.seek(0)

    # Choose a random line from the file and print it
    line = 0
    randomline = random.randint(0, linecount)
    while line < randomline:
        fh.readline()
        line += 1
    print fh.readline()

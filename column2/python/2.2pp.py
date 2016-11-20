#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Problem Statement:
    Give a sequential file that contains at most four billion 32-bit integers
in random order, find a 32-bit integer that isn't in the file (and there must
be at least one missing - why?). How would you solve this problem with ample
quantities of main memory? How would you solve it if you could use several
external "scratch" files but only a few hundred bytes of main memory?
Complexity: TODO
Usage:
    2.2pp randomints
    2.2pp run <input>
'''

# libraries
import sys
import os
import random


# functions
def genrandom(positions):
    '''
    Function to generate a file of random numbers from 0 to 2^32 - 1
    '''
    with open('random32bit.txt', 'w') as rfile:
        r = 0
        while r < 2**positions:
            rfile.write(str(r) + '\n')
            r += 1


def answer(infile, positions):
    '''
    Function to solve problem 2.2 from column 2 of Programming Pearls.
    '''
    # generate bitstring
    bitstring = ['0' for x in range(positions)]

    # start binary search
    scratch = infile
    for i in range(positions):

        # flip ith bit
        bitstring[i] = '1'

        # bitstring to int
        mask = int(''.join(bitstring), 2)

        # reset score
        score = [0, 0]

        # open files
        with open(scratch, 'r') as randomints, \
             open('0.{0}.txt'.format(i+1), 'w') as zeros, \
             open('1.{0}.txt'.format(i+1), 'w') as ones:

            # for number in file
            for number in randomints.readlines():

                # bitwise surgery
                bit = (mask & int(number)) >> (positions - 1 - i)

                # calculate score
                score[bit] += 1

                # sort to output files
                if bit:
                    # write to 1.txt
                    ones.write(number)
                else:
                    # write to 0.txt
                    zeros.write(number)

        # flip bit back
        bitstring[i] = '0'

        # finally
        if min(score):
            scratch = '{0}.{1}.txt'.format(score.index(min(score)), i+1)
        else:
            # when score minimum reaches zero
            return (score.index(min(score)) << (positions-1-i)) & int(number)


# executable
if __name__ == '__main__':

    # executable import only
    from docopt import docopt

    # check CLA
    args = docopt(__doc__)

    # flow
    if args['randomints']:
        # gen random 32bit integers
        genrandom(4)

    elif args['run']:
        # run binary search
        print answer(args['<input>'], 4)

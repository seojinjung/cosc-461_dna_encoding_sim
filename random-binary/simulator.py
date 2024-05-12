"""
SIMULATION.PY INPUTS: input file, encoding output file, data output file, coverage, error chance distributions
SIMULATION.PY OUTPUTS: an official encoding file and an output file
"""

# import libraries and other scripts
import logging
import sys
import argparse

#local imports
import encode
import pool
import error_injection
import decode

#vars

# read_args function: handles argument passing/parsing
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--file_in", help="file to encode", required = True)
    parser.add_argument("--out", help = "File with decoded message", required = True)
    parser.add_argument("--dna_out", help = "File with DNA oligos", required = True)
    parser.add_argument("--c", help = "Coverage", required = True)
    parser.add_argument("--e", help = "error rate distribution [pI,pD,pS]", required = True)
    args = parser.parse_args()
    args.orf = None

    return args

# readFile function: returns contents of file (as text)
def readFile(file_in):
    # open file
    try:
        f = open(file_in, 'rb')
    except:
        logging.error("%s file not found", file_in)
        sys.exit(0)

    data = f.read()
    # test prints
    # print(x)
    # print(data)

    return data

"""
todo:
MOVE THE COMMAND LINES TO SIMULATION.PY
SIMULATION.PY INPUTS: input file, encoding output file, data output file, coverage, error chance distributions
SIMULATION.PY OUTPUTS: an official encoding file and an output file
  -read text from input file
  -need simulator.py: break into pools. write pools (official encoding) to text?
  -THEN can do actual simulation on official encoding: 
    error injection,
    multiply strands x100 or so, 
    shuffle, 
    try to order and decode
  -send decode 
  """

#I don't know how to access the args so just pretend that IN is the file_in argument and OUT is out

"""
input_text = readFile(IN)

#For big data, would need to break into pools. for now, just one pool.


"""
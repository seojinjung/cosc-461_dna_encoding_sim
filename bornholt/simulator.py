"""
SIMULATION.PY INPUTS: input file, encoding output file, data output file, coverage, error chance distributions
SIMULATION.PY OUTPUTS: an official encoding file and an output file
"""

# import libraries and other scripts
import logging
import sys
import argparse
import random
import math

#local imports
import encode
import pool
import error_injection
import decode

#vars

# read_args function: handles argument passing/parsing
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_in", help="file to encode", required = True)
    parser.add_argument("--file_out", help = "File with decoded message", required = True)
    parser.add_argument("--file_dna_out", help = "File with DNA oligos", required = True)
    parser.add_argument("--c", help = "Coverage", required = True)
    args = parser.parse_args()
    args.orf = None

    return args

# readFile function: returns contents of file (as text)
def readFile(file_in):
    # open file
    try:
        f = open(file_in)
    except:
        logging.error("%s file not found", file_in)
        sys.exit(0)

    data = f.read()
    f.close()

    return data

# readFile function: returns contents of file (as text)
def writeFile(file_out, data):
    # open file
    try:
        f = open(file_out, "w")
    except:
        logging.error("%s file not found", file_out)
        sys.exit(0)
    
    f.write(data)
    f.close()

    return data

#I don't know how to access the args so just pretend that IN is the file_in argument and OUT is out
def main():
    #make the pool
    BYTES_PER_BLOCK = 12
    args = read_args()
    input_text = readFile(args.file_in)
    POOL = pool.makePool(input_text, BYTES_PER_BLOCK)
    ADDR_BITS = math.ceil(math.log2(len(POOL))) #number of address bits. same equation as in pool.py
    if (ADDR_BITS == 0): ADDR_BITS = 1
    DATA_BITS = BYTES_PER_BLOCK * 8

    #print(str(input_text))
    #print(POOL)

    #write the pool (no error added) encoding to file_dna_out
    dna_out = args.file_dna_out
    poolText = "~~~~ Encoding Report ~~~~ \n\nORIGINAL TEXT: \n" + input_text + "\n"
    poolText = poolText + "Total strands: " + str(len(POOL)) + "\n"
    poolText = poolText + "Coverage: " + str(args.c) + "\n"
    #poolText = poolText + "Error rates: " + str(args.e) + "\n\n"
    poolText = poolText + "-------------------------------POOL------------------------------------\n\n"
    for line in POOL:
        poolText = poolText + line + "\n"
    writeFile(dna_out, poolText)

    #now that I have the POOl, can do coverage
    COVERAGE = int(args.c)
    SIM_POOL = list() #the actual simulated pool. messier and way larger
    for strand in POOL:
        for i in range(COVERAGE):  #make more variable than just coverage? give or take?
            print(i, "\n")
            errorStrand = strand
            #print("This is the strand before error")
            #print(errorStrand)
            #errorStrand = error_injection.injectError(strand)
            #print("This is the strand after error")
            #print(errorStrand)
            SIM_POOL.append(errorStrand)
    #SHUFFLE!!!!
    random.shuffle(SIM_POOL)

    #now that I have the simulated pool, try to re-order and decode
    strandsByAddress = dict() #dictionary of key=adress and value=list of data with that address
    
    #one by one, read a strand
    for strand in SIM_POOL:
        binaryString = decode.BornholtDecoding(strand)
        #print("String:", binaryString)
        address = binaryString[:ADDR_BITS]
        data = strand[ADDR_BITS:]

        #sort by address
        if (strandsByAddress.get(address) == None): 
            strandsByAddress[address] = [strand]
            #print(strandsByAddress[address])
        else: 
            strandsByAddress[address].append(strand)
    #print (strandsByAddress)
    
    #MAJORITY VOTE
    sortedDecodedStrands = list()
    for i in range(len(POOL)): sortedDecodedStrands.append(" ")
    for key in strandsByAddress:
        #print("Key:", key)
        print(strandsByAddress[key])
        print(DATA_BITS)
        majorityStrandBin = decode.majorityVote(strandsByAddress[key], len(strandsByAddress[key][0]))
        majorityStrandBinary = decode.BornholtDecoding(majorityStrandBin)
        #print("Majority Guy:", majorityStrandBinary)
        majorityStrandString = decode.binaryToString(majorityStrandBinary)
        keyAsInt = int(key, 2)
        #if statement to catch rogue incorrectly address strands
        if (keyAsInt <= (len(sortedDecodedStrands) -1)): sortedDecodedStrands[keyAsInt] =  majorityStrandString

    FINAL_TEXT = ""
    for i in sortedDecodedStrands: FINAL_TEXT = FINAL_TEXT + i

    print(FINAL_TEXT)

    #print to DNA_OUT

main()
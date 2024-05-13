"""
SIMULATION.PY INPUTS: input file, encoding output file, data output file, coverage, error chance distributions
SIMULATION.PY OUTPUTS: an official encoding file and an output file
"""

# import libraries and other scripts
import binascii
import logging
import sys
import argparse
import random
import math
from difflib import SequenceMatcher

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
    parser.add_argument("--t", help = "How many times to run the sim", required = True)
    args = parser.parse_args()
    args.orf = None

    return args

# readAsBinary function: read in file as binary
def readAsBinary(file_in):
    # open file
    try:
        f = open(file_in, 'rb')
    except:
        logging.error("%s file not found", file_in)
        sys.exit(0)

    x = '' # hex

    # first translate to hex
    for chunk in iter(lambda: f.read(32), b''):
            x += str(binascii.hexlify(chunk)).replace("b","").replace("'","")

    # then translate hex to binary
    data  = bin(int(x, 16)).replace('b','')

    # test prints
    # print(x)
    # print(data)

    f.close()

    return data

# readAsText function: returns contents of file (as text)
def readAsText(file_in):
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
    input_bin = readAsBinary(args.file_in)
    expected_nts = int(len(input_bin) / 2)
    # print("input binary:", input_bin)
    POOL = pool.makePool(input_bin, BYTES_PER_BLOCK)
    ADDR_BITS = math.ceil(math.log2(len(POOL))) #number of address bits. same equation as in pool.py
    if (ADDR_BITS <= 1): ADDR_BITS = 2
    DATA_BITS = BYTES_PER_BLOCK * 8

    #print(str(input_text))
    # print(POOL)

    #write the pool (no error added) encoding to file_dna_out
    dna_out = args.file_dna_out
    text = readAsText(args.file_in)
    poolText = "~~~~ Encoding Report ~~~~ \n\nORIGINAL TEXT: \n" + text + "\n"
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
            errorStrand = strand
            #print("This is the strand before error")
            #print(errorStrand)
            errorStrand = error_injection.injectError(strand)
            #print("This is the strand after error")
            #print(errorStrand)
            SIM_POOL.append(errorStrand)
    #SHUFFLE!!!!
    random.shuffle(SIM_POOL)

    #now that I have the simulated pool, try to re-order and decode
    strandsByAddress = dict() #dictionary of key=adress and value=list of data with that address
    
    #one by one, read a strand
    for strand in SIM_POOL:
        binaryString = decode.DNAToBin(strand)
        address = binaryString[:ADDR_BITS]
        addr_nts = int(ADDR_BITS / 2)
        data = strand[addr_nts:] # dont worry about it

        #sort by address
        if (strandsByAddress.get(address) == None): 
            strandsByAddress[address] = [data]
            #print(strandsByAddress[address])
        else: 
            strandsByAddress[address].append(data)
    print (strandsByAddress)
    
    #MAJORITY VOTE
    sortedDecodedStrands = list()
    for i in range(len(POOL)): sortedDecodedStrands.append(" ")
    for key in strandsByAddress:
        # print(strandsByAddress[key])
        majorityStrandNT = decode.majorityVote(strandsByAddress[key], expected_nts)
        # print(majorityStrandNT)
        majorityStrandBinary = decode.DNAToBin(majorityStrandNT)
        # print(majorityStrandBinary)
        majorityStrandString = decode.binToText(majorityStrandBinary)
        # print(majorityStrandString)
        keyAsInt = int(key, 2)
        #if statement to catch rogue incorrectly address strands
        if (keyAsInt <= (len(sortedDecodedStrands) -1)): sortedDecodedStrands[keyAsInt] =  majorityStrandString

        FINAL_TEXT = ""
    for i in sortedDecodedStrands: FINAL_TEXT = FINAL_TEXT + i
    #STRIP NULL CHARACTERS FROM THE END
    while(FINAL_TEXT[-1] == chr(0)):
        FINAL_TEXT = FINAL_TEXT[:-1]
    return FINAL_TEXT

def errorRate(string1, string2):
    similarity = SequenceMatcher(None, string1, string2).ratio()
    return (1.0-similarity)*100

args = read_args()
outputs = list()
errorRates = list()
timesRun = int(args.t)
input_text = readAsText(args.file_in)

for i in range(timesRun):
    output = main()
    outputs.append(output)
    errorRates.append(errorRate(input_text, output))

#WRITE UP RESULTS
averageError = sum(errorRates)/len(errorRates)
resultPrint = "RESULTS\n\nRan (" + str(timesRun) + ") times.\nCoverage: " + str(args.c) + "\nAverage error: " + str(averageError) + "%\n\nList of outputs:\n"
i = 0
for o in outputs: 
    resultPrint = resultPrint + o + "\n   Error: " + str(errorRates[i]) + "%\n"
    i  = i + 1
out = args.file_out
writeFile(out, resultPrint)
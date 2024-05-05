'''
encode.py - simulates encoding files into DNA sequences using naive quaternary encoding and no error correction.

PARAMETERS:
    'file_in' - DNA-encoded file
    'out'     - decoded output file
'''

# import libraries and other scripts
import logging
import sys
import argparse

# read_args function: handles argument passing/parsing
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_in", help="file with DNA to decode", required = True)
    parser.add_argument("--out", help = "decoded file", required = True)
    args = parser.parse_args()
    args.orf = None

    return args

# readDNA function: read file and grab DNA sequence
def readDNA(file_in):
    # open file
    try:
        f = open(file_in)
    except:
        logging.error("%s file not found", file_in)
        sys.exit(0)
    
    data = f.read()

    return data

# DNAToBin function: takes DNA and translates it back into binary
def DNAToBin(dna):
    bin = ""
    #   print("dna to decode: ", dna)
    for i in dna:
        if i == "A":
            bin += "00"
        elif i == "C":
            bin += "01"
        elif i == "G":
            bin += "10"
        elif i == "T":
            bin += "11"
    #   print("decoded binary: ", bin)

    # convert to proper binary and return
    return int(bin, 2).to_bytes((len(bin) + 7) // 8, byteorder='big')

# main function: takes file argument, decodes the DNA to binary, and outputs the decoded file
def main():
    args = read_args()

    # read DNA-encoded file
    input = readDNA(args.file_in)
    
    decoded = DNAToBin(input)

    # write output to file
    out = open(args.out, 'wb')
    out.write(decoded)
    out.close()

# ----
main()
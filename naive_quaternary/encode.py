'''
encode.py - simulates encoding files into DNA sequences using naive quaternary encoding and no error correction.

PARAMETERS:
    'file_in' - any file
    'out'     - output file (DNA)
'''

# import libraries and other scripts
import binascii
import logging
import sys
import argparse
from error_injection import arterror

logging.basicConfig(level=logging.DEBUG)

# read_args function: handles argument passing/parsing
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_in", help="file to encode", required = True)
    parser.add_argument("--out", help = "File with DNA oligos", required = True)
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

# binToDNA function: convert binary data to dna nucleotides
def binToDNA(bin):
    g = [bin[i:i+2] for i in range(0, len(bin), 2)]
    # print("chunked: ", g)
    dna = ""

    for i in g:
        if i == "00":
            dna += "A"
        elif i == "01":
            dna += "C"
        elif i == "10":
            dna += "G"
        elif i == "11":
            dna += "T"
    
    # print("translated dna sequence: ", dna)
    return dna

# homopolymer function: calculates homopolymer runs of 3+ bases
def homopolymer(dna):
    runs = [] # list of all 3+ runs found
    homopolymerRun = 0 # current run
    cur = None # current character (for comparisons)

    for i in dna:
      if i == cur: 
        homopolymerRun += 1
      else:
        if homopolymerRun > 2:
          runs.append((homopolymerRun, cur)) # (number of repeats), (base)
        cur = i
        homopolymerRun = 1

    if homopolymerRun > 2:
      runs.append((homopolymerRun, cur))

    # print(runs)

    result = [len(runs), max(runs)] # (total number of runs), (longest homopolymer)
    return result

# gc function: calculates gc content (%)
def gc(dna):
   gc_count = 0

   for i in dna:
      if i == 'C' or i == 'G':
         gc_count += 1

   percent = round((gc_count / len(dna)) * 100, 2)
   return percent


# main function: takes file argument, translates to binary, and outputs a DNA sequence
def main():
    args = read_args()
    
    # read file as binary
    print('reading file.')
    binput = readAsBinary(args.file_in)
    
    # to human readable DNA
    output = binToDNA(binput)

    # inject errors
    # output = arterror(output, "insertion", 0.004)
    # output = arterror(output, "deletion", 0.1135)
    # output = arterror(output, "substitution", 0.003)

    # results of homopolymer + gc tests
    homopolymers = homopolymer(output)
    print("total homopolymer runs:", homopolymers[0])
    print("longest homopolymer run:", homopolymers[1]) # not necessarily the only run with this length
    gcs = gc(output)
    print("gc content:", str(gcs) + "%")

    # write output to file
    out = open(args.out, 'w')
    out.write(output)
    out.close()
    print("file", args.out, "created.")

# ---
main()
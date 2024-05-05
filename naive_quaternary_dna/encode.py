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

    return data

def binToDNA(bin):
  g = [bin[i:i+2] for i in range(0, len(bin), 2)]
#   print("chunked: ", g)
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
#   print("final dna sequence: ", dna)
  return dna

# main function: takes file argument, translates to binary, and outputs a DNA sequence
def main():
    args = read_args()

    # read file as binary
    binput = readAsBinary(args.file_in)
    
    # to human readable DNA
    output = binToDNA(binput)

    # write output to file
    out = open(args.out, 'w')
    out.write(output)
    out.close()

# ----
main()
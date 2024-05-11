'''
encode.py - simulates encoding files into DNA sequences using naive quaternary encoding and no error correction.

PARAMETERS:
    'file_in' - any file
    'out'     - output file (DNA)

@seojin
'''

# import libraries and other scripts
import binascii
import logging
import sys
import argparse
import random

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

# copied from wendy's code thank u wendy
# Artificially insert error into a string of bits
# PARAMETERS: 'bits' - string; bits in which to add error
#             'type' - string; accepts 'insertion', 'deletion', and 'substitution'
#             'chance' - float; accepts a fraction for chance of error appearing
def arterror (bits, type, chance):
    # Convert the string to a list for easier manipulation
    bits_list = list(bits)
    nucleotides = ['A', 'C', 'G', 'T']

    # ---------------------------------------------------------------------------

    # Artificially add insertion error
    if type == "insertion":
      for i in range(len(bits_list)):
          if random.random() < chance:
              # Insert a random bit (0 or 1) at the current position
              bits_list.insert(i, str(random.choice(nucleotides)))

    # ---------------------------------------------------------------------------

    # Artificially add deletion error
    elif type == "deletion":
      # Track the indices of bits to delete
      indices_to_delete = []

      # Identify indices to delete based on the error chance
      for i in range(len(bits_list)):
          if random.random() < chance:
              indices_to_delete.append(i)

      # Delete bits from the list based on the identified indices
      for i in reversed(indices_to_delete):
          del bits_list[i]

    # ---------------------------------------------------------------------------

    # Artificially add substitution error
    elif type == "substitution":
      for i in range(len(bits_list)):
        if random.random() < chance:
          # Flips the bit: 0 becomes 1, 1 becomes 0
          bits_list[i] = random.choice(nucleotides)

    # ---------------------------------------------------------------------------

    else:
      print("Invalid Error Type!")

    # Convert the list back to a string
    error_str = ''.join(bits_list)
    print(type, "error added with a", chance, "chance:", error_str)
    return error_str

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
          runs.append((cur * homopolymerRun, homopolymerRun))
        cur = i
        homopolymerRun = 1

    if homopolymerRun > 2:
      runs.append((cur * homopolymerRun, homopolymerRun))

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
    binput = readAsBinary(args.file_in)
    
    # to human readable DNA
    output = binToDNA(binput)

    # inject errors
    output_w_err = arterror(output, "insertion", 1/1000)
    output_w_err = arterror(output_w_err, "deletion", 1/1000)
    output_w_err = arterror(output_w_err, "substitution", 1/500)

    # results of homopolymer + gc tests
    homopolymers = homopolymer(output_w_err)
    logging.info("total homopolymer runs: ", homopolymers[0])
    logging.info("longest homopolymer run: ", homopolymers[1]) # not necessarily the only run with this length
    gcs = gc(output_w_err)
    logging.info("gc content: ", str(gcs) + "%")

    # write output to file
    out = open(args.out, 'w')
    out.write(output)
    out.close()
    logging.info("file %s created.", output)

# ----
main()
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
import random

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
    # return int(bin, 2).to_bytes((len(bin) + 15) // 16, byteorder='little')

    # alternate version where it stays a string
    # return bin

def binToText(bin):
    ret = ""
    thisByte = ""
    for c in bin:
        thisByte = thisByte + c
        if (len(thisByte) == 8):
            #convert to number then character
            char = chr(int(thisByte, 2))
            ret = ret + char
            thisByte = ""
    return ret

#takes in a list of strands (in NTs) and averages them out to make a final strand
#needs the theoretical length of a perfect strand (no indels)
def majorityVote(strandList, theoreticalLength):
  #print("Majority vote called. theoretical length ", theoreticalLength, " num strands ", len(strandList))
  #print(strandList)
  finalStrand = ""
  nucleotideVotes = {'A' : 0, 'C' : 0, 'T' : 0, 'G' : 0,}
  for i in range(theoreticalLength):
    nextChar = ""
    #tally the "votes" from all the strands
    for strand in strandList:
      if (i <= (len(strand)-1)):
        vote = strand[i]
        nucleotideVotes[vote] = nucleotideVotes.get(vote, 0) + 1
    #catch exception: zero votes because all strands got deletion errors (this is highly unlikely but could break code)
    if (nucleotideVotes['A'] == 0 and nucleotideVotes['C'] == 0 and nucleotideVotes['T'] == 0 and nucleotideVotes['G'] == 0):
      nts = ['C', 'A','T','G']
      nextChar = random.choice(nts)
    #otherwise: choose whichever nt got the most "votes"
    else:
      nextChar = max(nucleotideVotes, key=nucleotideVotes.get)
    finalStrand = finalStrand + nextChar
    nucleotideVotes = {'A' : 0, 'C' : 0, 'T' : 0, 'G' : 0,} # reset  
  return finalStrand

def majorityVoteBin(strandList, theoreticalLength):
  #print("Majority vote called. theoretical length ", theoreticalLength, " num strands ", len(strandList))
  #print(strandList)
  finalStrand = ""
  nucleotideVotes = {'1' : 0, '0' : 0}
  for i in range(theoreticalLength):
    nextChar = ""
    #tally the "votes" from all the strands
    for strand in strandList:
      if (i <= (len(strand)-1)):
        vote = strand[i]
        nucleotideVotes[vote] = nucleotideVotes.get(vote, 0) + 1
    #catch exception: zero votes because all strands got deletion errors (this is highly unlikely but could break code)
    if (nucleotideVotes['1'] == 0 and nucleotideVotes['0'] == 0):
      bins  = ['1', '0']
      nextChar = random.choice(bins)
    #otherwise: choose whichever nt got the most "votes"
    else:
      nextChar = max(nucleotideVotes, key=nucleotideVotes.get)
    finalStrand = finalStrand + nextChar
    nucleotideVotes = {'1' : 0, '0' : 0} # reset
  return finalStrand
#testList = ['GC', 'GC', 'GT']
#print(majorityVote(testList, 3))

# main function: takes file argument, decodes the DNA to binary, and outputs the decoded file
def main():
    args = read_args()

    # read DNA-encoded file
    print("reading file.")
    input = readDNA(args.file_in)

    print("nucs:", len(input))
    
    decoded = DNAToBin(input)
    
    # write output to file
    out = open(args.out, 'wb')
    out.write(decoded)
    out.close()
    print("saved file as", args.out)
# ----
main()
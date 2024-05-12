"""
DECODE.PY

The end.

(string_of_nucleotides) turns nt back to binary

TODO: 
    -decodeStrand is specifically meant to turn back to binary. need to turn back to characters?
"""
import random

def ntToBinary(baseString):
  ret = ""
  for c in baseString:
    nextChar = '0'
    if (c == 'T' or c == 'G'): nextChar = '1'
    ret += nextChar
  return ret

def binaryToString(binString):
  ret = ""
  thisByte = ""
  for c in binString:
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
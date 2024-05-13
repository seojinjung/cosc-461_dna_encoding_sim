"""
DECODE.PY

The end.

(string_of_nucleotides) turns nt back to binary

TODO: 
    -decodeStrand is specifically meant to turn back to binary. need to turn back to characters?
"""
from heapq import heappush, heappop
import random
import itertools

# create a list of all possible k-length sequences of bits
def binseq(k):
    return [''.join(x) for x in itertools.product('01', repeat=k)]

## VVVVVVVVVVVV BORNHOLT DECODING METHOD BELOW VVVVVVVVVVVV

## ---------------- HUFFMAN SETUP ----------------

# Set up our little tree guy
class Node:
    def __init__(self, symbol=None, freq=None):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.mid = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build frequency tables based on how often our values show up
def build_frequency_table(input_string):
    freq_table = {}
    for symbol in input_string:
        if symbol in freq_table:
            freq_table[symbol] += 1
        else:
            freq_table[symbol] = 1
    return freq_table

# Build the little tree guy
def build_huffman_tree(freq_table):
    heap = []
    for symbol, freq in freq_table.items():
        heappush(heap, Node(symbol, freq))

    while len(heap) > 1:
        left = heappop(heap)
        mid = heappop(heap)
        right = None  # Placeholder for right child

        if heap:  # Ensure heap is not empty before popping
            right = heappop(heap)

        combined_freq = left.freq + mid.freq + (right.freq if right else 0)
        new_node = Node(freq=combined_freq)
        new_node.left = left
        new_node.mid = mid
        new_node.right = right

        heappush(heap, new_node)

    return heap[0]  # Root of the Huffman tree

# Generate our Huffman Codes
def generate_huffman_codes(node, current_code="", codes={}):
    if node:
        if node.symbol is not None:
            codes[node.symbol] = current_code
        else:
            generate_huffman_codes(node.left, current_code + "0", codes)
            generate_huffman_codes(node.mid, current_code + "1", codes)
            generate_huffman_codes(node.right, current_code + "2", codes)
    return codes

# The overall process of Huffman-ing
def huffman(input_string):
    freq_table = build_frequency_table(input_string)
    huffman_tree = build_huffman_tree(freq_table)
    huffman_codes = generate_huffman_codes(huffman_tree)
    return huffman_codes

## ---------------- BASES BACK TO HUFFMAN CODE ----------------

def bases_to_huffman(bases):
  bits_list = list(bases)
  strand = ''
  for i in range(len(bits_list)):
    if(i > 0):
      prev = bases[i-1]
    if(i == 0 or prev == 'A'):
      if(bits_list[i] == 'C'):
        strand = strand + '0'
      elif(bits_list[i] == 'G'):
        strand = strand + '1'
      elif(bits_list[i] == 'T'):
        strand = strand + '2'
    elif(prev == 'C'):
      if(bits_list[i] == 'G'):
        strand = strand + '0'
      elif(bits_list[i] == 'T'):
        strand = strand + '1'
      elif(bits_list[i] == 'A'):
        strand = strand + '2'
    elif(prev == 'G'):
      if(bits_list[i] == 'T'):
        strand = strand + '0'
      elif(bits_list[i] == 'A'):
        strand = strand + '1'
      elif(bits_list[i] == 'C'):
        strand = strand + '2'
    elif(prev == 'T'):
      if(bits_list[i] == 'A'):
        strand = strand + '0'
      elif(bits_list[i] == 'C'):
        strand = strand + '1'
      elif(bits_list[i] == 'G'):
        strand = strand + '2'
  return strand

## ---------------- HUFFMAN CODE BACK TO BITS ----------------

def huffman_decode(huffman_codes, decoded_bits):
    decoded_str = ''
    current_code = ''
    
    # Walk through each bit until we have something that matches a key
    for bit in decoded_bits:
        current_code += bit
        if current_code in huffman_codes.values():
            decoded_str += next(key for key, value in huffman_codes.items() if value == current_code)
            current_code = '' 
            print("Decoded String:", decoded_str)
            
    return decoded_str

## ---------------- BITS BACK TO STRING ----------------

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

## ---------------- BORNHOLT DECODING ----------------

def BornholtDecoding(encoded_bases):
   # Initialize our Huffman Encoding
  binseq8 = binseq(8)
  huffman_codes = huffman(binseq8)

  print("STEP 1 - ENCODED BASES:", encoded_bases)
  # Bases to Huffman
  decoded_huffman = bases_to_huffman(encoded_bases)
  print("STEP 2 - BASE TO HUFFMAN:", decoded_huffman)

  # Huffman to bits
  decoded_bits = huffman_decode(huffman_codes, decoded_huffman)
  print("STEP 3 - HUFFMAN TO BITS", decoded_bits)

  print("\n")

  return decoded_bits

## VVVVVVVVVVVV POOLING SCHMOOLING BELOW VVVVVVVVVVVV

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
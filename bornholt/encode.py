"""
ENCODE.PY

Turns text into nucleotide sequences. Uses RANDOM BINARY encoding described by Church et. al

Key functions:
    toBinary(string)
    toRandomNucleotides(binary_sequence)
"""

import itertools
from heapq import heappush, heappop

# convert input string to binary (ascii?)
def toBinary(a):
  charList,binList=[],[]
  for i in a:
    charList.append(ord(i))
  for i in charList:
    binStr = str(bin(i)[2:])
    while len(binStr) < 8: binStr = '0' + binStr #pad w/ leading zeroes
    binList.append(binStr)
  s = ''.join(str(b) for b in binList)
  return s

# create a list of all possible k-length sequences of bits
def binseq(k):
    return [''.join(x) for x in itertools.product('01', repeat=k)]

## VVVVVVVVVVVV BORNHOLT ENCODING METHOD BELOW VVVVVVVVVVVV

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

## ---------------- BITS TO HUFFMAN CODE ----------------

def bits_to_huffman(huffman_codes, bits):
    encoded_str = ''
    current_code = ''
    
    # Walk through each bit until we have something that matches a key
    for bit in bits:
        current_code += bit
        if current_code in huffman_codes.keys():
            encoded_str += huffman_codes[current_code]
            current_code = '' 
            
    # Return our encoded bits        
    return encoded_str

## ---------------- HUFFMAN CODE TO BASES GENERATION ----------------

# Convert Huffman Code to Bases
def huffman_to_bases(bits):
  # Bit list!
  bits_list = list(bits)
  # Initialize the strand we're gonna return
  strand = ''
  # Implement a rotating encoding scheme
  for i in range(len(bits_list)):
    # Edge case
    if(i > 0):
      prev = strand[i-1]
    # If previous nucleotide is A
    if(i == 0 or prev == 'A'):
      if(bits_list[i] == '0'):
        strand = strand + 'C'
      elif(bits_list[i] == '1'):
        strand = strand + 'G'
      elif(bits_list[i] == '2'):
        strand = strand + 'T'
    # If previous nucleotide is C
    elif(prev == 'C'):
      if(bits_list[i] == '0'):
        strand = strand + 'G'
      elif(bits_list[i] == '1'):
        strand = strand + 'T'
      elif(bits_list[i] == '2'):
        strand = strand + 'A'
    # If previous nucleotide is G
    elif(prev == 'G'):
      if(bits_list[i] == '0'):
        strand = strand + 'T'
      elif(bits_list[i] == '1'):
        strand = strand + 'A'
      elif(bits_list[i] == '2'):
        strand = strand + 'C'
    # If previous nucleotide is T
    elif(prev == 'T'):
      if(bits_list[i] == '0'):
        strand = strand + 'A'
      elif(bits_list[i] == '1'):
        strand = strand + 'C'
      elif(bits_list[i] == '2'):
        strand = strand + 'G'
  # Return our little DNA strand
  return strand

## ---------------- BORNHOLT ENCODING ----------------

def BornholtEncoding(binary_bits):
  # Initialize our Huffman Encoding
  binseq8 = binseq(8)
  huffman_codes = huffman(binseq8)

  # Convert bits to Huffman
  huffman_bits = bits_to_huffman(huffman_codes, binary_bits)

  # Convert Huffman to Nucleotides
  encoded_bases = huffman_to_bases(huffman_bits)

  return encoded_bases
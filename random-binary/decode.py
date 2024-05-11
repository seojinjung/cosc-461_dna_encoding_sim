"""
DECODE.PY

The end.

decodeStrand(string_of_nucleotides) turns nt back to binary

TODO: 
    -decodeStrand is specifically meant to turn back to binary. need to turn back to characters?
"""

def decodeStrand(baseString):
  ret = ""
  for c in baseString:
    nextChar = '0'
    if (c == 'T' or c == 'G'): nextChar = '1'
    ret += nextChar
  return ret
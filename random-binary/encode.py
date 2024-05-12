"""
ENCODE.PY

Turns text into nucleotide sequences. Uses RANDOM BINARY encoding described by Church et. al

Key functions:
    toBinary(string)
    toRandomNucleotides(binary_sequence)
"""

import random

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

# convert binary sequence to nucleotides
def toNucleotides(binarySequence):
  #return value: the calculated sequence of bases
  ret = ''
  gcc = 0 # GC Content
  gcCounter = 0 # total GC counter
  homopolymerRun = 0 #number of same bases in a row

  for b in binarySequence:
    # 50 / 50 chance
    coinFlip = random.randint(0, 1)
    #determine the next base
    nextBase = ''

    #FROM HOLY GRAIL: Church rules were *no more than 3 homopolyer run and ~50% GC content*

    if (b == '0'):
      #options are A or C. if all is well (GC content under 50%, homopolymer run of 2 or less), just follow coin flip
      atHomopolymerRisk = homopolymerRun >= 3 and (ret[-1] == 'A' or ret[-1] == 'C')
      if (gcc < 0.5 and not atHomopolymerRisk):
        #print("Standard procedure")
        #standard procedure
        if (coinFlip == 0): nextBase = 'A'
        else: nextBase = 'C'

      #I assume it's better to avoid homopolymer than it is to reduce GC content, so firstly do that
      # print("Avoiding homopolymers")
      if (atHomopolymerRisk and ret[-1] == 'A'): nextBase = 'C'
      if (atHomopolymerRisk and ret[-1] == 'C'): nextBase = 'A'

      #if homopolymer is not a risk but GC content is >0.5, just choose A to reduce GC content
      if (not atHomopolymerRisk and gcc >= 0.5): nextBase = 'A'

    #COPIED ABOVE LOGIC
    if (b == '1'):
      #options are T or G. if all is well (GC content under 50%, homopolymer run of 2 or less), just follow coin flip
      atHomopolymerRisk = homopolymerRun >= 3 and (ret[-1] == 'G' or ret[-1] == 'T')
      if (gcc < 0.5 and not atHomopolymerRisk):
        #print("Standard procedure")
        #standard procedure
        if (coinFlip == 0): nextBase = 'G'
        else: nextBase = 'T'

      # print("Avoiding homopolymers")
      if (atHomopolymerRisk and ret[-1] == 'G'): nextBase = 'G'
      if (atHomopolymerRisk and ret[-1] == 'T'): nextBase = 'T'

      #if homopolymer run is not a risk but GC content is >0.5, just choose T to reduce GC content
      if (not atHomopolymerRisk and gcc >= 0.5): nextBase = 'T'

    #append!
    ret += nextBase

    #update homopolymer run (only do once there is already one base)
    if (len(ret) >= 2):
      #check for a new homopolymer run
      if (homopolymerRun == 0):
        if (ret[-1] == ret[-2]): homopolymerRun = 2
      #check for continuing homopolymer or reset
      else:
        if (ret[-1] == ret[-2]): homopolymerRun += 1
        else: homopolymerRun = 0
    #print(homopolymerRun)

    #update GC content
    if (nextBase == 'G' or nextBase == 'C'): gcCounter += 1
    gcc = gcCounter / len(ret)

  #print("Final GC Content: ", round(gcc, 4)*100, "%") #for debugging
  return ret

# putting it together: take in an input string, output a nucleotide sequence
def stringToNucleotides(inputString):
  return toNucleotides(toBinary(inputString))
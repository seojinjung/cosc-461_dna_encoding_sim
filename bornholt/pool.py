"""
POOL.PY

Organizes blocks of data into pools.

key function is makePool(input_data_as_text, block_size_in_bytes) 
"""

import math
import encode

#SPLIT TO BLOCKS. takes an INPUT STRING and the SIZE OF EACH BLOCK (in bytes!)
def splitToBlocks (inputString, blockSize):
  counter = 0
  thisBlock = ""
  blocksList = list()
  for char in inputString:
    counter += 1
    thisBlock += char
    if ((counter % blockSize)== 0):
      blocksList.append(thisBlock)
      thisBlock = ""
    #end of string: add blank spaces
    elif (counter == len(inputString)):
      for i in range(blockSize - (counter % blockSize)): thisBlock += "0" #ASCII character 00000000 is NULL
      blocksList.append(thisBlock)
  return blocksList

#ADD ADDRESS BITS: takes in a list and adds appropriate amount of bits based on size of list
def addAddressBits (blocksList):
  newList = list()
  #calculate number of address bits
  poolSize = len(blocksList)
  numBits = math.ceil(math.log2(poolSize))
  #print("Pool size ", poolSize, ". Num of bits", numBits)
  #add the bits!
  addr = 0b0
  for block in blocksList:
    tempFormat = '0' + str(numBits) + 'b' #just a custom format argument to fit the appropriate number of bits
    addrFormatted = format(addr, tempFormat)
    newList.append(addrFormatted +block)
    addr += 1
  return newList

# going to skip primers since we are not actually conducting PCR

#composite function to take data and return a pool
def makePool(inputString, blockSize):
    #convert data to binary, binary to blocks, add address bits, then to bases?
    dataInBinary = encode.toBinary(inputString)
    addressedDataInBinary = addAddressBits(splitToBlocks(dataInBinary, blockSize*8))
    addressedDataInBases = list()
    #TO BASES!
    for b in addressedDataInBinary:
      addressedDataInBases.append(encode.BornholtEncoding(b))
    return addressedDataInBases

#testers
"""
BLOCK_SIZE = 12

INPUT1 = "All"
INPUT2 = "Second sentences can be zany and crazy."
INPUT3 = "Third string for a third pool and a longer sentence"

POOLS = list()
POOLS.append(makePool(INPUT1, BLOCK_SIZE)) #can streamline this if doing several pools
POOLS.append(makePool(INPUT2, BLOCK_SIZE))
POOLS.append(makePool(INPUT3, BLOCK_SIZE))

for p in POOLS: print(p)
"""
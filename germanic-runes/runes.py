# Imports and libraries
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import cm
from matplotlib import pyplot as plt

# Run Length Encoding
# PARAMETERS: 'matrix' - ndarray; a matrix to encode.
def encoderunlength(matrix):

    # Flatten our matrix into a string
    string = ''.join(map(str, matrix.flatten()))
    # Initialize some stuff
    result = ''
    n = len(string)
    i = 0

    # Walk through each character of the string
    while i < n- 1:

        # Count occurrences of current character
        count = 1
        while (i < n - 1 and string[i] == string[i + 1]):
            count += 1
            # Increment inner while-loop
            i += 1
        # Increment outer while-loop
        i += 1

        # Append the appropriate nucleotide based on character count
        if(count==1):
          result = result + "C"
        elif (count==2):
          result = result + "T"
        elif (count==3):
          result = result + "A"
        elif (count==4):
          result = result + "G"
    return result


# Run length decoding
# PARAMETERS: 'dna' - string; a string of nucleotides
#             'rows/columns' - ints; define a rows x columns matrix
def decoderunlength(dna, rows, columns):

    # Initialize some stuff
    result = ''
    n = len(dna)
    i = 0
    # Start our binary list at 1
    binary = 1

    # Walk through each nucleotide in string
    while i <= n- 1:
        # Based on the nucleotide, add 1/2/3/4 copies of 0/1 to our result
        if(dna[i]=="C"):
          result = result + (str(binary) * 1)
        elif (dna[i]=="T"):
          result = result + (str(binary) * 2)
        elif (dna[i]=="A"):
          result = result + (str(binary) * 3)
        elif (dna[i]=="G"):
          result = result + (str(binary) * 4)

        # Alternate our binary number
        if(binary == 0):
          binary += 1
        elif(binary == 1):
          binary -= 1

        # Increment the while-loop
        i += 1

    # Convert the list of binary numbers into an array
    arr = np.array(list(result), dtype=int)
    # Reshape the array into an rows x columns matrix
    decodedmatrix = arr.reshape(rows, columns)

    # Return the original matrix
    return decodedmatrix

# Define our germanic rune matrix
germanic = np.array([[1, 0, 1, 0 ,1],
                   [0, 1, 1, 1 ,0],
                   [0, 0, 1, 0 ,0],
                   [0, 0, 1, 0 ,0],
                   [0, 0, 1, 0 ,0],
                   [0, 0, 1, 0 ,0],
                   [0, 0, 1, 0 ,0],])

print("GIVEN: \n", germanic)
# Encode the matrix, print the result
encoded_germanic = encoderunlength(germanic)
print("ENCODED:", encoded_germanic)
# Decode the matrix, print the result
decoded_germanic = decoderunlength(encoded_germanic, 7, 5)
print("DECODED: \n", decoded_germanic)


# Convert our decoded matrix to a pixel image
def pixels(pixelmatrix):
  plt.imshow(pixelmatrix, interpolation='nearest',cmap='binary')
  plt.show()

pixels(decoded_germanic)
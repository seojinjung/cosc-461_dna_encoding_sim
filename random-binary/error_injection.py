# Imports and libraries
import random

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

"""
string = "CCCCCCAACGCGCGCGCT"
arterror(string, "insertion", 1/1000)
arterror(string, "deletion", 1/1000)
arterror(string, "substitution", 1/500)
"""
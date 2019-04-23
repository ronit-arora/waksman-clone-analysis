import blaster
import placedata

# Sequence
test_query = 'AGGCGAAGGAGAAAGAGAAAGAGGAGTGAGCAGAGTTACTTCAGCGATGGAAGGCCAGGAGCAGCTGGTAAAACCGCGGGTTATGAAGGTGGAGTCGGAGGAATCATGGAATGTCATCACTGCCGAGGCGAAAACCCAAGGTTGCCCGGTGTTCGTCCACTTCATGGCTTCATGGTGCGTCCCGTCCGTGGCAATGAACCCTTTCTTCGAAGCTCTTGCGCAGAGCTATCAGGATGTGCTCTTCCTCCTGGTGGATGTTGACGCCGCTAAGGCCGTGGCAACCAGAATGGGGGTGAAGGCCATGCCCACATTCCTGCTCTTAAGTGAGGGCTGCGTCGTGGATAAGATAGTGGGAGCCAACCCCGATGAGATAAGGAAGAGGATGGATGGGTTCATCCATTCCTTTCACCGCCCCTCAGAGGTGGAGAGCATTTAAGAGGCTTCAGTTTCTTGTGCTCACGAACCAAAGATGGTCAGCTCGGGGTTTCTTGTGAATACCTCCTCCGTGAATAAATAACACGGCTCTCTCTCTCTCTTTCTCTCTCTCTGTCTCTCTGTCTCTCTCTCTCTCTCACTATTTCTTCTCTCTTCCTGCCACGTGTAGAATTATAAGAATCCAGTTATTTTGTAAAAACTAGTCTTGTTCAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
print("Before Starting Program - Success")

# Getting the JSON data for the nr search
blastn_nr = blaster.blaster(test_query, 'blastn', 'nr')
print("Retrieving blastn nr data: Successful")

# Getting the JSON data for the est search
blastn_est = blaster.blaster(test_query, 'blastn', 'est')
print("Retrieving blastn est data: Successful")

blastx_nr = blaster.blaster(test_query, 'blastx', 'nr')
print("Retrieving blastx nr data: Successful")

# Initializing a placedata instantiation with test_query
writer = placedata.PlaceData(test_query)

print('Successfully initialized my writer')

# Writing JSON data to xls file
writer.blastn_write(blastn_nr, blastn_est)

print('Succesfully wrote blastn data to excel')





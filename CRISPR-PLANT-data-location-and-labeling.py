import csv

# Define the sequences for the UTR and exons. That's the place, where you want to put your target sequences
utr = "CCGTTTCACTCACTCGGCCTCTCCACTCCACTCATCCGGCCATTAACGACGAGCAGGCAACTCGCAATAGTATTATCCACACCACAACATTCGTGTGCACCTTCTCCCCACATCCATCGCGGTCACCGCCGGTACAACTAATCAAGCTGCCAGCCTCGTACTCACGATACCCTCGCCAGCTCTGGACGGTATAAATTCACCATCCACCGTACAGTTACCTCAAGACGTTCTCCTCTTCTCCCACCGGTCTGGTTTAACTGTGTTGCC"
exon_1 = "ATGGCCCAAGAACGGGAGCCGCTCCTGCAGAACGGCGGCAATGCCGCCGGGGCCAAGGGCTCGCCTGCTCTGCTGCCGTCCCTGGCCAGGTCCGTGCTCAAGTTCCTCATGTGGGCGGTGTTCCTCACCTGGGCCGGAGGGATCTTCTTCTACCCCACGAAGCCCGTGCAGGCCGCGTTCCAGGAGTGGGCGGGGGTCACCAAGCAGTCCCTCTTCGGCATCACCG"
utr_exon_1 = utr + exon_1 # Combined UTR and exon 1 sequences zone
exon_2 = "GGACCGTTTTTCTTGCCTTCAGCGCGCCGATTCTGATCGTTGCGGCTCTTGCCTATGTGTACATCGCCGCCTTCCCTAATGATCATATCGA"

regions = {"utr": utr, "exon_1": exon_1, "utr_exon_1": utr_exon_1, "exon_2": exon_2}

in_path = "/Users/ulianadoroshenko/Downloads/data.csv" # Unlocated data from CRIPSR-PLANT
out_path = "/Users/ulianadoroshenko/Downloads/data_labeled.csv" # CRISPR-PLANT loation labeled and location limited data in format (SeqID, minMM_GG, minMM_AG, spacer seq, PAM, strand, location)

# Read the input CSV, label sequences based on defined regions, and write to the output CSV
input_file = open(in_path, newline="")
output_file = open(out_path, "w", newline="")

reader = csv.reader(input_file)
writer = csv.writer(output_file)

header = next(reader)       # the first line is the column names
writer.writerow(header)

found_count = 0
not_found_count = 0

for row in reader:
    spacer = row[3].upper()   # 4th column = spacer sequence (Python counts from 0)

    # Make the reverse complement (the same sequence read 5'->3' on the other DNA strand)
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    reverse_complement = ""
    for letter in spacer:
        reverse_complement = complement[letter] + reverse_complement

    location = ""             # stays empty if the spacer is not found
    for name in regions:
        if spacer in regions[name] or reverse_complement in regions[name]:
            location = name
            break             # stop at the first region that matches

    if location == "":
        not_found_count = not_found_count + 1
    else:
        row[6] = location     # 7th column = location
        writer.writerow(row)
        found_count = found_count + 1

input_file.close()
output_file.close()

print("Found in a region:", found_count)
print("Not found:", not_found_count)


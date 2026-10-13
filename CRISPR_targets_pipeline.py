import csv

# Combines the three steps of the pipeline in one script:
#   1. CRISPR-PLANT-data-location-and-labeling.py - label CRISPR-PLANT spacers by gene region
#   2. CRISPOR_and_CRISPR-PLANT.py - add CRISPOR scores
#   3. CRISPR-P_and_merged_data.py - add CRISPR-P scores

# Define the sequences for the UTR and exons. That's the place, where you want to put your target sequences
utr = "CCGTTTCACTCACTCGGCCTCTCCACTCCACTCATCCGGCCATTAACGACGAGCAGGCAACTCGCAATAGTATTATCCACACCACAACATTCGTGTGCACCTTCTCCCCACATCCATCGCGGTCACCGCCGGTACAACTAATCAAGCTGCCAGCCTCGTACTCACGATACCCTCGCCAGCTCTGGACGGTATAAATTCACCATCCACCGTACAGTTACCTCAAGACGTTCTCCTCTTCTCCCACCGGTCTGGTTTAACTGTGTTGCC"
exon_1 = "ATGGCCCAAGAACGGGAGCCGCTCCTGCAGAACGGCGGCAATGCCGCCGGGGCCAAGGGCTCGCCTGCTCTGCTGCCGTCCCTGGCCAGGTCCGTGCTCAAGTTCCTCATGTGGGCGGTGTTCCTCACCTGGGCCGGAGGGATCTTCTTCTACCCCACGAAGCCCGTGCAGGCCGCGTTCCAGGAGTGGGCGGGGGTCACCAAGCAGTCCCTCTTCGGCATCACCG"
utr_exon_1 = utr + exon_1 # Combined UTR and exon 1 sequences zone
exon_2 = "GGACCGTTTTTCTTGCCTTCAGCGCGCCGATTCTGATCGTTGCGGCTCTTGCCTATGTGTACATCGCCGCCTTCCCTAATGATCATATCGA"

regions = {"utr": utr, "exon_1": exon_1, "utr_exon_1": utr_exon_1, "exon_2": exon_2}

plant_path = "/Users/ulianadoroshenko/Downloads/data.csv" # Unlocated data from CRISPR-PLANT in format (SeqID, minMM_GG, minMM_AG, spacer seq, PAM, strand, location)
crispor_path = "/Users/ulianadoroshenko/Downloads/CRISPOR - no CRISPR-PLANT.csv" # CRISPOR data in format (targetSeq, mitSpecScore, cfdSpecScore, offtargetCount, Doench '16-Score)
crispr_p_path = "/Users/ulianadoroshenko/Downloads/CRISPR-P_no_merge.csv" # CRISPR-P data in format (Num, On-score, Sequence, Region, %GC)
out_path = "/Users/ulianadoroshenko/Downloads/data_merged_CRISPOR_CRISPR-PLANT_CRISPR-P.csv" # Location labeled CRISPR-PLANT data with CRISPOR and CRISPR-P scores added

crispor_columns = ["mitSpecScore", "cfdSpecScore", "offtargetCount", "Doench '16-Score"]
crispr_p_columns = ["On-score", "%GC"]


# Read a CRISPOR or CRISPR-P table and remember the scores of every spacer
def read_scores(path, sequence_column, score_columns):
    file = open(path, newline="")
    reader = csv.DictReader(file)   # DictReader lets us use column names, e.g. row["On-score"]

    scores_by_spacer = {}
    for row in reader:
        # Sequence = 20 letter spacer + 3 letter PAM, CRISPR-PLANT gives only the 20 letter spacer
        spacer = row[sequence_column].upper()[:20]
        scores = []
        for column in score_columns:
            scores.append(row[column])
        scores_by_spacer[spacer] = scores

    file.close()
    return scores_by_spacer


crispor_scores = read_scores(crispor_path, "targetSeq", crispor_columns)
crispr_p_scores = read_scores(crispr_p_path, "Sequence", crispr_p_columns)

# Read the CRISPR-PLANT CSV, label sequences based on defined regions, add the scores, and write to the output CSV
input_file = open(plant_path, newline="")
output_file = open(out_path, "w", newline="")

reader = csv.reader(input_file)
writer = csv.writer(output_file)

header = next(reader)       # the first line is the column names
writer.writerow(header + crispor_columns + crispr_p_columns)

found_count = 0
not_found_count = 0
no_crispor_count = 0
no_crispr_p_count = 0

for row in reader:
    spacer = row[3].upper()   # 4th column = spacer sequence (Python counts from 0)

    # Step 1: find the region of the spacer

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
        continue              # skip spacers that are not in any region
    found_count = found_count + 1
    row[6] = location         # 7th column = location

    # Step 2: add CRISPOR scores
    if spacer in crispor_scores:
        row = row + crispor_scores[spacer]
    else:
        row = row + ["", "", "", ""]   # keep the row, but leave the scores empty
        no_crispor_count = no_crispor_count + 1
        print("No CRISPOR scores for", spacer, "in", location)

    # Step 3: add CRISPR-P scores
    if spacer in crispr_p_scores:
        row = row + crispr_p_scores[spacer]
    else:
        row = row + ["", ""]   # keep the row, but leave the scores empty
        no_crispr_p_count = no_crispr_p_count + 1
        print("No CRISPR-P scores for", spacer, "in", location)

    writer.writerow(row)

input_file.close()
output_file.close()

print("Found in a region:", found_count)
print("Not found:", not_found_count)
print("Rows without CRISPOR scores:", no_crispor_count)
print("Rows without CRISPR-P scores:", no_crispr_p_count)

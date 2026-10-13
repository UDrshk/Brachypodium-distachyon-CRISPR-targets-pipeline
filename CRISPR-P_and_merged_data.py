import csv

merged_path = "/Users/ulianadoroshenko/Downloads/data_merged_CRISPOR_and_CRISPR-PLANT.csv" # CRISPR-PLANT data with CRISPOR scores from CRISPOR_and_CRISPR-PLANT.py
crispr_p_path = "/Users/ulianadoroshenko/Downloads/CRISPR-P_no_merge.csv" # CRISPR-P data in format (Num, On-score, Sequence, Region, %GC)
out_path = "/Users/ulianadoroshenko/Downloads/data_merged_CRISPOR_CRISPR-PLANT_CRISPR-P.csv" # Merged data with CRISPR-P scores added

score_columns = ["On-score", "%GC"]

# Read the CRISPR-P table and remember the scores of every spacer
crispr_p_file = open(crispr_p_path, newline="")
crispr_p_reader = csv.DictReader(crispr_p_file)   # DictReader lets us use column names, e.g. row["On-score"]

crispr_p_scores = {}
for row in crispr_p_reader:
    # CRISPR-P Sequence = 20 letter spacer + 3 letter PAM, CRISPR-PLANT gives only the 20 letter spacer
    spacer = row["Sequence"].upper()[:20]
    scores = []
    for column in score_columns:
        scores.append(row[column])
    crispr_p_scores[spacer] = scores

crispr_p_file.close()

# Read the merged table, add the CRISPR-P scores to every row, and write to the output CSV
merged_file = open(merged_path, newline="")
output_file = open(out_path, "w", newline="")

reader = csv.reader(merged_file)
writer = csv.writer(output_file)

header = next(reader)       # the first line is the column names
writer.writerow(header + score_columns)

found_count = 0
not_found_count = 0

for row in reader:
    spacer = row[3].upper()   # 4th column = spacer sequence

    if spacer in crispr_p_scores:
        writer.writerow(row + crispr_p_scores[spacer])
        found_count = found_count + 1
    else:
        writer.writerow(row + ["", ""])   # keep the row, but leave the scores empty
        not_found_count = not_found_count + 1
        print("No CRISPR-P scores for", spacer, "in", row[6])

merged_file.close()
output_file.close()

print("Rows with CRISPR-P scores:", found_count)
print("Rows without CRISPR-P scores:", not_found_count)

import csv

plant_path = "/Users/ulianadoroshenko/Downloads/data_labeled.csv" # Location labeled data from CRISPR-PLANT-data-location-and-labeling.py
crispor_path = "/Users/ulianadoroshenko/Downloads/CRISPOR - no CRISPR-PLANT.csv" # CRISPOR data in format (targetSeq, mitSpecScore, cfdSpecScore, offtargetCount, Doench '16-Score)
out_path = "/Users/ulianadoroshenko/Downloads/data_merged_CRISPOR_and_CRISPR-PLANT.csv" # CRISPR-PLANT data with CRISPOR scores added

score_columns = ["mitSpecScore", "cfdSpecScore", "offtargetCount", "Doench '16-Score"]

# Read the CRISPOR table and remember the scores of every spacer
crispor_file = open(crispor_path, newline="")
crispor_reader = csv.DictReader(crispor_file)   # DictReader lets us use column names, e.g. row["mitSpecScore"]

crispor_scores = {}
for row in crispor_reader:
    # CRISPOR targetSeq = 20 letter spacer + 3 letter PAM, CRISPR-PLANT gives only the 20 letter spacer
    spacer = row["targetSeq"].upper()[:20]
    scores = []
    for column in score_columns:
        scores.append(row[column])
    crispor_scores[spacer] = scores

crispor_file.close()

# Read the CRISPR-PLANT table, add the CRISPOR scores to every row, and write to the output CSV
plant_file = open(plant_path, newline="")
output_file = open(out_path, "w", newline="")

reader = csv.reader(plant_file)
writer = csv.writer(output_file)

header = next(reader)       # the first line is the column names
writer.writerow(header + score_columns)

found_count = 0
not_found_count = 0

for row in reader:
    spacer = row[3].upper()   # 4th column = spacer sequence

    if spacer in crispor_scores:
        writer.writerow(row + crispor_scores[spacer])
        found_count = found_count + 1
    else:
        writer.writerow(row + ["", "", "", ""])   # keep the row, but leave the scores empty
        not_found_count = not_found_count + 1
        print("No CRISPOR scores for", spacer, "in", row[6])

plant_file.close()
output_file.close()

print("Rows with CRISPOR scores:", found_count)
print("Rows without CRISPOR scores:", not_found_count)

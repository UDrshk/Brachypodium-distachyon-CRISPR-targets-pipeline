# Brachypodium-distachyon-CRISPR-targets-pipeline
Pipeline for target definition for Brachypodium distachyon CRISPR

# Platforms used

https://crispor.gi.ucsc.edu/crispor.py - CRISPOR\
http://crispr.hzau.edu.cn/cgi-bin/CRISPR2/CRISPR - CRISPR-P v. 2.0\
https://omap.org/crispr/CRISPRsearch.html - CRISPR-PLANT\
NCBI and Phytozome genomic databases

# How to use

There are two ways to use this pipeline:
- **Beginners:** use one script, `CRISPR_targets_pipeline.py`, which runs all steps at once. Follow the quick start below.
- **Advanced users:** use the three separate scripts, which run one step each and save a file after every step. See [Step-by-step scripts](#step-by-step-scripts-advanced).

## Quick start (for beginners)

### What you need
- **Python 3.** To check if you have it, open Terminal (Mac) or Command Prompt (Windows) and type `python3 --version`. If you see a version number like `Python 3.12.1`, you are ready. If not, download Python from https://www.python.org/downloads/. No extra packages are needed.
- **This repository.** On GitHub, click the green **Code** button, then **Download ZIP**, and unzip it.

### Step 1. Get your gene sequences
Go to Phytozome or NCBI and copy the sequences of the gene parts where you want to put your target: the 5' UTR, exon 1 and exon 2. Copy them 5'→3' in the direction of the gene.

### Step 2. Get the three tables of targets
Run your gene on each platform and save each result as a **CSV** file. The first row of every file must be the column names.

| Platform | Columns the file must have |
|---|---|
| CRISPR-PLANT | `SeqID, minMM_GG, minMM_AG, Spacer seq (5'->3'), PAM (5'->3'), strand, location`, in this order |
| CRISPOR | `targetSeq, mitSpecScore, cfdSpecScore, offtargetCount, Doench '16-Score` |
| CRISPR-P v. 2.0 | `Num, On-score, Sequence, Region, %GC` |

CRISPOR and CRISPR-P files may have extra columns, but the column names above must be spelled exactly the same.

### Step 3. Put your data into the script
Open `CRISPR_targets_pipeline.py` in any text editor (for example VS Code) and change only the top part:
1. Paste your sequences between the quotes of `utr = "..."`, `exon_1 = "..."` and `exon_2 = "..."`.
2. Change the four paths so they point to your files:
   - `plant_path` – your CRISPR-PLANT table
   - `crispor_path` – your CRISPOR table
   - `crispr_p_path` – your CRISPR-P table
   - `out_path` – where the result should be saved (this file will be created)

   Tip: on a Mac, right-click a file in Finder, hold the **Option** key and click **Copy "…" as Pathname** to get its full path.

### Step 4. Run the script
In Terminal, go to the folder with the script and run it:
```
cd path/to/Brachypodium-distachyon-CRISPR-targets-pipeline
python3 CRISPR_targets_pipeline.py
```
In VS Code you can also open the script and click the ▶ (Run) button in the top right corner.

### Step 5. Check the result
The script prints a short summary, for example:
```
Found in a region: 42
Not found: 346
Rows without CRISPOR scores: 1
Rows without CRISPR-P scores: 0
```
- **Found in a region** – targets that are in your UTR, exon 1 or exon 2. Only these are saved.
- **Not found** – targets from other parts of the gene. They are left out.
- **Rows without … scores** – targets that the platform did not score. They are still saved, but those score cells are empty. The script prints each of them, so you know which ones.

Open the file from `out_path` in Excel. Each target now has its region in the `location` column and the CRISPOR and CRISPR-P scores in the last columns.

### Common problems
- **`FileNotFoundError`** – a path in Step 3 is wrong. Check the spelling and that the file ends with `.csv`.
- **`KeyError: 'targetSeq'`** (or another column name) – a column in your CRISPOR or CRISPR-P file has a different name. Rename it to match the table in Step 2.
- **`KeyError: 'N'`** (or another letter) – a CRISPR-PLANT spacer has a letter other than A, C, G or T.

## Step-by-step scripts (advanced)
The quick start script does the same work as these three scripts. Use them if you want to see or check the result of every step. Run them in this order. Each one reads the file made by the one before it:

| Order | Script | What it does | Saves |
|---|---|---|---|
| 1 | `CRISPR-PLANT-data-location-and-labeling.py` | Finds which region (UTR, exon 1, UTR/exon 1 border, exon 2) each CRISPR-PLANT target is in, and removes the rest | `data_labeled.csv` |
| 2 | `CRISPOR_and_CRISPR-PLANT.py` | Adds the CRISPOR scores | `data_merged_CRISPOR_and_CRISPR-PLANT.csv` |
| 3 | `CRISPR-P_and_merged_data.py` | Adds the CRISPR-P scores | `data_merged_CRISPOR_CRISPR-PLANT_CRISPR-P.csv` |

As in the quick start, change the paths at the top of each script before running it.

## Data preparation
### CRISPR-PLANT data labeling
Because CRISPR-PLANT as a platform does focus on the whole gene as a region of interest and label only utr/exon/introne difference, we want to clear our data from targets that are not located on the begging of the genomic sequence.
1. Go to CRISPR-PLANT, and get the sequence list in format: [SeqID, minMM_GG, minMM_AG, spacer seq, PAM, strand, location]
2. Go to Phytozome or NCBI database to get your genome sequence, where you plan to put your target
3. Open CRISPR-PLANT-data-location-and-labeling.py and modify 4th row by putting your zones of interest in
4. Run and get CRISPR-PLANT sequences that are located in your region of interest

### 

## Data processing
## Results

# How it works

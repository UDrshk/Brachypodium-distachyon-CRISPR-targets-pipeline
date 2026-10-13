# Brachypodium-distachyon-CRISPR-targets-pipeline
Pipeline for target definition for Brachypodium distachyon CRISPR

# Platforms used

https://crispor.gi.ucsc.edu/crispor.py - CRISPOR\
http://crispr.hzau.edu.cn/cgi-bin/CRISPR2/CRISPR - CRISPR-P v. 2.0\
https://omap.org/crispr/CRISPRsearch.html - CRISPR-PLANT\
NCBI and Phytozome genomic databases

# How to use
## Data preparation
### CRISPR-PLANT data labeling
Because CRISPR-PLANT as a platform does focus on the whole gene as a region of interest and label only utr/exon/introne difference, we want to clear our data from targets that are not located on the begging of the genomic sequence.
1. Go to CRISPR-PLANT, and get the sequence list in format: [SeqID, minMM_GG, minMM_AG, spacer seq, PAM, strand, location]
2. Go to Phytozome or NCBI database to get your genome sequence, where you plan to put your target
3. Open CRISPR-PLANT-data-location_and_labeling.py and modify 4th row by putting your zones of interest in
4. Run and get CRISPR-PLANT sequences that are located in your region of interest

### 

## Data processing
## Results

# How it works

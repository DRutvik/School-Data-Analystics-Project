# School Data Cleaning and Merging Project

## Overview
This project is a Python script that cleans and merges student assessment data from multiple schools. The raw data files often have inconsistent column names, missing values, and extra characters (like `*` in growth target columns). The script standardizes, cleans, and combines all the data into a single, ready-to-use CSV file.

---

## Features
- Reads multiple raw CSV files for different schools.
- Normalizes column names and renames them to a standard format.
- Cleans growth target columns by removing unwanted characters (`*`) and filling missing values with `"Unknown"`.
- Cleans Math and Reading scores, replacing blanks or invalid values with `"Unknown"`.
- Converts IDs and scores to integer type while keeping missing values as `<NA>`.
- Converts and forward-fills missing test dates.
- Removes exact duplicate rows and duplicate students per school.
- Merges all school datasets into one final CSV.

---

## Files
- `process_assessment.py` – Main Python script for cleaning and merging the data.
- `merged_all_schools.csv` – Output file with all schools’ data merged.
- `schoolA.csv`, `schoolB.csv`, `schoolC.csv`, `schoolD.csv`, `schoolE.csv` – Example raw input files.

---

## How to Use
1. Place all raw school CSV files in the same folder as `process_assessment.py`.
2. Make sure the `raw_files` list in the script contains all filenames you want to process.
3. Run the script:
   ```bash
   python process_assessment.py

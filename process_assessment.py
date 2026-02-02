import pandas as pd

# List of raw school files
raw_files = ["schoolA.csv","schoolB.csv", "schoolC.csv", "schoolD.csv", "schoolE.csv"]

# Mapping messy column names to standard names
COLUMN_RENAME_MAP = {
    "studentid": "StudentID",
    "student_id": "StudentID",
    "schoolid": "SchoolID",
    "school_id": "SchoolID",
    "seasonyear": "Season_Year",
    "season_year": "Season_Year",
    "testdate": "Test_Date",
    "test_date": "Test_Date",
    "mathematics_score": "Mathematics_Score",
    "mathematics_met_growth_target": "Mathematics_Met_Growth_Target",
    "reading_score": "Reading_Score",
    "reading_met_growth_target": "Reading_Met_Growth_Target"
}

all_dfs = []

for file in raw_files:
    # Read the CSV file
    df = pd.read_csv(file, sep=None, engine="python")
    
    # Normalize column names
    df.columns = (df.columns.str.strip().str.replace("\ufeff", "", regex=False).str.lower().str.replace(" ", "_")
    )
    
    # Rename columns to standard names
    df = df.rename(columns=COLUMN_RENAME_MAP)
    
    # Drop rows where all values are empty
    df = df.dropna(how='all')
    
    # Clean growth target columns (remove * and fix blanks)
    for col in df.columns:
        if "growth" in col.lower():
            df[col] = (df[col].astype(str).str.replace("*", "", regex=False).str.strip().replace(["nan", "None", "", "N/A", "--"], "Unknown").fillna("Unknown"))
    
    # Clean Math & Reading scores, replace blanks with "Unknown"
    for score_col in ["Mathematics_Score", "Reading_Score"]:
        if score_col in df.columns:
            df[score_col] = df[score_col].astype(str).str.strip()
            df[score_col] = df[score_col].replace(["", " ", "nan", "None", "--"], "Unknown")
            df[score_col] = df[score_col].fillna("Unknown")
    
    # Convert IDs and scores to integers (keep Unknown as <NA>)
    for col in ["StudentID", "SchoolID", "Mathematics_Score", "Reading_Score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    
    # Convert dates and forward-fill missing values
    if "Test_Date" in df.columns:
        df["Test_Date"] = pd.to_datetime(df["Test_Date"], errors="coerce")
        df["Test_Date"] = df["Test_Date"].ffill()
    
    # Remove exact duplicate rows
    df = df.drop_duplicates()
    
    # Add cleaned dataframe to the list
    all_dfs.append(df)

# Merge all school dataframes
all_schools = pd.concat(all_dfs, ignore_index=True)

# Remove duplicate students in the same school
if {"StudentID", "SchoolID"}.issubset(all_schools.columns):
    all_schools = all_schools.drop_duplicates(subset=["StudentID", "SchoolID"],keep="first")

# Save final merged CSV
all_schools.to_csv("merged_all_schools.csv", index=False)

print("All schools cleaned and merged successfully")
print("Final dataset shape:", all_schools.shape)
print("Column data types:")
print(all_schools.dtypes)

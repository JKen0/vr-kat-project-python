import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-WALK-3.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
walk3a_extracted_rows = df.iloc[list(range(2553, 5543))]

# Create a new CSV file
walk3a_extracted_rows.to_csv(EXTRACT_FOLDER_PATH + "PRE-TRAIN-WALK-3A.xlsx", index=False)
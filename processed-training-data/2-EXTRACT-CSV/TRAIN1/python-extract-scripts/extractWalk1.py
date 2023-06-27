import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-WALK-1.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
walk1a_extracted_rows = df.iloc[list(range(2339, 5449))]
walk1b_extracted_rows = df.iloc[list(range(7605, 11374))]

# Create a new CSV file
walk1a_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-WALK-1A.xlsx", index=False)
walk1b_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-WALK-1B.xlsx", index=False)
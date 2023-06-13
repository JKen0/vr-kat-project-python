import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-WALK-2.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
walk2a_extracted_rows = df.iloc[list(range(2532, 5538))]
walk2b_extracted_rows = df.iloc[list(range(6273, 9648))]

# Create a new CSV file
walk2a_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-WALK-2A.xlsx", index=False)
walk2b_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-WALK-2B.xlsx", index=False)
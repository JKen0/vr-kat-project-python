import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-STANDING.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
stand1_extracted_rows = df.iloc[list(range(2924, 3377))]
stand2_extracted_rows = df.iloc[list(range(3526, 4630))]
stand3_extracted_rows = df.iloc[list(range(4835, 5424))]

# Create a new CSV file
stand1_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-STAND1.xlsx", index=False)
stand2_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-STAND2.xlsx", index=False)
stand3_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-STAND3.xlsx", index=False)
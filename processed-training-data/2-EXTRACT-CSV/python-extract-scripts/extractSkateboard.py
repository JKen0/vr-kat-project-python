import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-SKATEBOARD.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
large_fast_extracted_rows = df.iloc[list(range(4070, 7085))]

# Create a new CSV file
large_fast_extracted_rows.to_csv(EXTRACT_FOLDER_PATH + "PRE-TRAIN-SKATEBOARD.csv", index=False)

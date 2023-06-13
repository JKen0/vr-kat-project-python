import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-SMALL-WALK.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
small_walk_extracted_rows = df.iloc[list(range(1907, 4722))]

# Create a new CSV file
small_walk_extracted_rows.to_csv(EXTRACT_FOLDER_PATH + "PRE-TRAIN-SMALL-WALK.csv", index=False)

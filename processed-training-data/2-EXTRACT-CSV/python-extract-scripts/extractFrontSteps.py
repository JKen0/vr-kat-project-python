import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-FRONT-STEPS.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
small_step_extracted_rows = df.iloc[list(range(2545, 6333))]
medium_step_extracted_rows = df.iloc[list(range(7035, 10897))]
large_step_extracted_rows = df.iloc[list(range(11557, 16967))]

# Create a new CSV file
small_step_extracted_rows.to_csv(EXTRACT_FOLDER_PATH + "PRE-TRAIN-SMALL-STEPS.csv", index=False)
medium_step_extracted_rows.to_csv(EXTRACT_FOLDER_PATH + "PRE-TRAIN-MEDIUM-STEPS.csv", index=False)
large_step_extracted_rows.to_csv(EXTRACT_FOLDER_PATH + "PRE-TRAIN-LARGE-STEPS.csv", index=False)
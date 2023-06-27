import pandas as pd

RAW_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\RAW-TRAIN-SIDE-DIAGONAL-STEPS.csv"

EXTRACT_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\\"



# Read the original CSV file
df = pd.read_csv(RAW_FILE_PATH)

# Extract the rows
left_step_extracted_rows = df.iloc[list(range(1792, 4881))]
right_step_extracted_rows = df.iloc[list(range(5547, 8658))]
left_diag_step_extracted_rows = df.iloc[list(range(9536, 12584))]
right_diag_step_extracted_rows = df.iloc[list(range(13035, 16201))]

# Create a new CSV file
left_step_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-LEFT-STEPS.xlsx", index=False)
right_step_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-RIGHT-STEPS.xlsx", index=False)
left_diag_step_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-LEFT-DIAG-STEPS.xlsx", index=False)
right_diag_step_extracted_rows.to_excel(EXTRACT_FOLDER_PATH + "PRE-TRAIN-RIGHT-DIAG-STEPS.xlsx", index=False)

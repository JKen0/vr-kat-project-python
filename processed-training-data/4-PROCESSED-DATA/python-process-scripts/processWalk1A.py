import pandas as pd

FILE_NAME = "WALK-1A"

PRE_TRAIN_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\PRE-TRAIN-" + FILE_NAME + ".xlsx"
PROCESS_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\PROCESSED-" + FILE_NAME + ".xlsx"

Z_VELOCITY_A = 4.00



# Read the XLSX file
df = pd.read_excel(PRE_TRAIN_FILE_PATH)

# DEFINE CONDITIONS
isStanding = df['Notes2'] == "STANDING"
isMotionA = df['Notes2'] == "MOTION_A"


df['X_Vel'] = 0.000

# Update the columns based on the conditions
df.loc[isStanding, 'Z_Vel'] = 0.000
df.loc[isMotionA, 'Z_Vel'] = Z_VELOCITY_A


# Save the modified DataFrame to a new XLSX file
df.to_excel(PROCESS_FILE_PATH, index=False)
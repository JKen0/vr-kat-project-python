import pandas as pd

FILE_NAME = "SMALL-WALK"

PRE_TRAIN_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\PRE-TRAIN-" + FILE_NAME + ".xlsx"
PROCESS_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\PROCESSED-" + FILE_NAME + ".xlsx"

Z_VELOCITY_A = 2.50
Z_VELOCITY_B = 4.00
Z_VELOCITY_C = 2.00



# Read the XLSX file
df = pd.read_excel(PRE_TRAIN_FILE_PATH)

# DEFINE CONDITIONS
isStanding = df['Notes'] == "STANDING"
isMotionA = df['Notes'] == "MOTION_A"
isMotionB = df['Notes'] == "MOTION_B"
isMotionC = df['Notes'] == "MOTION_C"


df['X_Vel'] = 0.000

# Update the columns based on the conditions
df.loc[isStanding, 'Z_Vel'] = 0.000
df.loc[isMotionA, 'Z_Vel'] = Z_VELOCITY_A
df.loc[isMotionB, 'Z_Vel'] = Z_VELOCITY_B
df.loc[isMotionC, 'Z_Vel'] = Z_VELOCITY_C



# Save the modified DataFrame to a new XLSX file
df.to_excel(PROCESS_FILE_PATH, index=False)
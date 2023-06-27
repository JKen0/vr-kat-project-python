import pandas as pd

FILE_NAME = "WALK-2A"

PRE_TRAIN_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\PRE-TRAIN-" + FILE_NAME + ".xlsx"
PROCESS_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\PROCESSED-" + FILE_NAME + ".xlsx"

Z_VELOCITY_A = 2.50
Z_VELOCITY_B = 3.50
Z_VELOCITY_C = 2.25
Z_VELOCITY_D = 4.50
Z_VELOCITY_E = 2.00


# Read the XLSX file
df = pd.read_excel(PRE_TRAIN_FILE_PATH)

# DEFINE CONDITIONS
isStanding = df['Notes2'] == "STANDING"
isMotionA = df['Notes2'] == "MOTION_A"
isMotionB = df['Notes2'] == "MOTION_B"
isMotionC = df['Notes2'] == "MOTION_C"
isMotionD = df['Notes2'] == "MOTION_D"
isMotionE = df['Notes2'] == "MOTION_E"


df['X_Vel'] = 0.000

# Update the columns based on the conditions
df.loc[isStanding, 'Z_Vel'] = 0.000
df.loc[isMotionA, 'Z_Vel'] = Z_VELOCITY_A
df.loc[isMotionB, 'Z_Vel'] = Z_VELOCITY_B
df.loc[isMotionC, 'Z_Vel'] = Z_VELOCITY_C
df.loc[isMotionD, 'Z_Vel'] = Z_VELOCITY_D
df.loc[isMotionE, 'Z_Vel'] = Z_VELOCITY_E


# Save the modified DataFrame to a new XLSX file
df.to_excel(PROCESS_FILE_PATH, index=False)
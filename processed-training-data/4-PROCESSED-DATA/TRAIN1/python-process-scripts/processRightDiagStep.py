import pandas as pd

FILE_NAME = "RIGHT-DIAG-STEPS"

PRE_TRAIN_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\2-EXTRACT-CSV\PRE-TRAIN-" + FILE_NAME + ".xlsx"
PROCESS_FILE_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\PROCESSED-" + FILE_NAME + ".xlsx"

X_VELOCITY = 1.500
Z_VELOCITY = 1.500


# Read the XLSX file
df = pd.read_excel(PRE_TRAIN_FILE_PATH)

# DEFINE CONDITIONS
beforeOrAfter = (df['Iteration'] < 13051) | (df['Iteration'] > 16201)


# Update the columns for every row
df['X_Vel'] = X_VELOCITY 
df['Z_Vel'] = Z_VELOCITY

# Update the columns based on the conditions
df.loc[beforeOrAfter, 'X_Vel'] = 0.000
df.loc[beforeOrAfter, 'X_Vel'] = 0.000




# Save the modified DataFrame to a new XLSX file
df.to_excel(PROCESS_FILE_PATH, index=False)
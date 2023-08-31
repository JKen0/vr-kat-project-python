import os
import pandas as pd
import numpy as np

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\\ADDITIONALUSER\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\\ADDITIONALUSER\\"

# FETCH ALL DATA
PROCESS_TRAIN2_FOLDER = "C:\\Dev\\vr-kat-project-python-2\\processed-training-data\\4-PROCESSED-DATA\\EXTRA\\"
ALL_FILE_NAMES = [file for file in os.listdir(SOURCE_FOLDER_PATH) if file.endswith('.csv')]

# Create empty dataframes df1 and df2
dfs1 = []
dfs2 = []
dfs3 = []

for fileConfig in ALL_FILE_NAMES:
    file_path = SOURCE_FOLDER_PATH + fileConfig

    # Read the Excel file
    df = pd.read_csv(file_path)

    df['L_Pitch_Delta'] = df['L_Pitch'].diff()
    df['L_Roll_Delta'] = df['L_Roll'].diff()
    df['R_Pitch_Delta'] = df['R_Pitch'].diff()
    df['R_Roll_Delta'] = df['R_Roll'].diff()

    # Conditional indexing to split data into df1 and df2
    condition1 = df['Notes1'].isin(['MOTION_A', 'STANDING_A'])
    condition2 = df['Notes1'].isin(['MOTION_B', 'STANDING_B'])
    condition3 = df['Notes1'].isin(['MOTION_C', 'STANDING_C'])
    
    dfs1.append(df[condition1])
    dfs2.append(df[condition2])
    dfs3.append(df[condition3])

    # Concatenate the dataframes in the lists to create df1 and df2
    df1 = pd.concat(dfs1, ignore_index=True)
    df2 = pd.concat(dfs2, ignore_index=True)
    df3 = pd.concat(dfs3, ignore_index=True)

    df1.to_excel(DESTINATION_FOLDER_PATH + "PROC-ADDITIONALUSER1-STEPS-LR-LAR-60BPM.xlsx", index=False)
    df2.to_excel(DESTINATION_FOLDER_PATH + "PROC-ADDITIONALUSER1-SIDESTEPS-L-LAR-60BPM.xlsx", index=False)
    df3.to_excel(DESTINATION_FOLDER_PATH + "PROC-ADDITIONALUSER1-SIDESTEPS-R-LAR-60BPM.xlsx", index=False)
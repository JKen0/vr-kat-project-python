import os
import pandas as pd
import numpy as np

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\\EXTRA\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\\EXTRA\\"

# FETCH ALL DATA
PROCESS_TRAIN2_FOLDER = "C:\\Dev\\vr-kat-project-python-2\\processed-training-data\\4-PROCESSED-DATA\\EXTRA\\"
ALL_FILE_NAMES = [file for file in os.listdir(SOURCE_FOLDER_PATH) if file.endswith('.csv') and "BSTEPS" in file]

for fileConfig in ALL_FILE_NAMES:
    file_path = SOURCE_FOLDER_PATH + fileConfig


    # Read the Excel file
    df = pd.read_csv(file_path)



    df['L_Pitch_Delta'] = df['L_Pitch'].diff()
    df['L_Roll_Delta'] = df['L_Roll'].diff()
    df['R_Pitch_Delta'] = df['R_Pitch'].diff()
    df['R_Roll_Delta'] = df['R_Roll'].diff()

    # Exclude rows where 'Notes1' is equal to 'CUTOFF'
    df = df[df['Notes1'] != 'CUTOFF']  

    df[['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['STEPS', 'BSTEPS', 'AVERAGE']

    df.to_excel(DESTINATION_FOLDER_PATH + 'PROC' + fileConfig[3:-4] + '.xlsx', index=False)
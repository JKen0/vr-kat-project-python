import os
import pandas as pd
import numpy as np

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\TRAIN2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"

# FETCH ALL DATA
PROCESS_TRAIN2_FOLDER = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"
ALL_FILE_NAMES = [file for file in os.listdir(SOURCE_FOLDER_PATH) if file.endswith('.xlsx') and "STAND" in file]


for fileConfig in ALL_FILE_NAMES:
    file_path = SOURCE_FOLDER_PATH + fileConfig

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Double the length of the DataFrame
    concat_df = pd.concat([df, df, df], ignore_index=True)
    
    concat_df['Iteration'] = range(len(concat_df))
    concat_df[['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']]= ['STAND', 'SML', 'SLOW']

    concat_df.to_excel(DESTINATION_FOLDER_PATH + 'PROC' + fileConfig[3:], index=False)
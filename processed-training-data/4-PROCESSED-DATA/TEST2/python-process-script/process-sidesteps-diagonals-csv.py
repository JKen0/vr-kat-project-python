import pandas as pd
import os

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\\TEST2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\\TEST2\\"

FILES_ARRAY = [
    {
        "fileName": "RAW-TEST2-DIAGONALS-LR-LAR-80BPM.csv", 
        "X_Vel_L": -0.646578, 
        "Z_Vel_L": 0.646578, 
        "destinationFileName_L": "PROC-TEST2-DIAGONALS-L-LAR-80BPM.xlsx",
        "X_Vel_R": 0.92, 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TEST2-DIAGONALS-R-LAR-80BPM.xlsx" 
    },
    {
        "fileName": "RAW-TEST2-SIDESTEPS-LR-MED-70BPM.csv", 
        "X_Vel_L": -0.82677, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TEST2-SIDESTEPS-L-MED-70BPM.xlsx",
        "X_Vel_R": 0.668131, 
        "Z_Vel_R": 0.668131, 
        "destinationFileName_R": "PROC-TEST2-SIDESTEPS-R-MED-70BPM.xlsx" 
    },
]

for fileConfig in FILES_ARRAY:
    file_path = SOURCE_FOLDER_PATH + fileConfig["fileName"]

    # Read the Excel file
    df = pd.read_csv(file_path)

    # Exclude rows where 'Notes1' is equal to 'CUTOFF'
    df = df[df['Notes1'] != 'CUTOFF']   

    # Filter the DataFrame for file A and B(STANDING_A and MOTION_A)
    file_a_df = df[df['Notes1'].isin(['STANDING_A', 'MOTION_A'])]
    file_b_df = df[df['Notes1'].isin(['STANDING_B', 'MOTION_B'])]

    # update values for file A
    file_a_df.loc[df['Notes1'] == 'STANDING_A', ['Notes1', 'X_Vel', 'Z_Vel']] = ['STANDING', 0, 0]
    file_a_df.loc[df['Notes1'] == 'MOTION_A', ['X_Vel', 'Z_Vel']] = [fileConfig["X_Vel_L"], fileConfig["Z_Vel_L"]]   


    # update values for file B
    file_b_df.loc[df['Notes1'] == 'STANDING_B', ['Notes1', 'X_Vel', 'Z_Vel']] = ['STANDING', 0, 0]
    file_b_df.loc[df['Notes1'] == 'MOTION_B', ['Notes1','X_Vel', 'Z_Vel']] = [ 'MOTION_A', fileConfig["X_Vel_R"], fileConfig["Z_Vel_R"]]   


    # save the modified csv to a spreadsheet
    file_a_df.to_excel(DESTINATION_FOLDER_PATH + fileConfig["destinationFileName_L"], index=False)
    file_b_df.to_excel(DESTINATION_FOLDER_PATH + fileConfig["destinationFileName_R"], index=False)
import pandas as pd

SOURCE_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\TRAIN2\\"
DESTINATION_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"

FILES_ARRAY = [
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-LAR-60BPM.csv", 
        "X_Vel_L": -0.92, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-LAR-60BPM.xlsx",
        "X_Vel_R": 0.92, 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-LAR-60BPM.xlsx" 
    },
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-LAR-80BPM.csv", 
        "X_Vel_L": -1.22 , 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-LAR-80BPM.xlsx",
        "X_Vel_R": 1.22, 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-LAR-80BPM.xlsx" 
    },
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-MED-80BPM.csv", 
        "X_Vel_L": -0.88, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-MED-80BPM.xlsx",
        "X_Vel_R": 0.88 , 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-MED-80BPM.xlsx" 
    },
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-MED-110BPM.csv", 
        "X_Vel_L": -1.21, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-MED-110BPM.xlsx",
        "X_Vel_R": 1.21, 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-MED-110BPM.xlsx" 
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
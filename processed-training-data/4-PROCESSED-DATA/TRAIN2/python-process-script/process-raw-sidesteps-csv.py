import pandas as pd
import os
import json 

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

# Open the config file and load its content into a dictionary
config_file = open(CURRENT_DIRECTORY + '\\config\\config.json')
CONFIG_DATA = json.load(config_file)

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\TRAIN2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"

# define BPM bounds between classes
UPPER_BOUND_SLOW_BPM = CONFIG_DATA['SIDESTEPS_UPPER_BOUND_SLOW_BPM']
UPPER_BOUND_MEDIUM_BPM = CONFIG_DATA['SIDESTEPS_UPPER_BOUND_AVERAGE_BPM']

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
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-LAR-82BPM.csv", 
        "X_Vel_L": -0.88, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-LAR-82BPM.xlsx",
        "X_Vel_R": 0.88 , 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-LAR-82BPM.xlsx" 
    },
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-LAR-110BPM.csv", 
        "X_Vel_L": -1.21, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-LAR-110BPM.xlsx",
        "X_Vel_R": 0.88 , 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-LAR-110BPM.xlsx" 
    },
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-SML-60BPM.csv", 
        "X_Vel_L": -0.88, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-SML-60BPM.xlsx",
        "X_Vel_R": 0.88 , 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-SML-60BPM.xlsx" 
    },
    {
        "fileName": "RAW-TRAIN2-SIDESTEPS-LR-SML-80BPM.csv", 
        "X_Vel_L": -1.21, 
        "Z_Vel_L": 0.00, 
        "destinationFileName_L": "PROC-TRAIN2-SIDESTEPS-L-SML-80BPM.xlsx",
        "X_Vel_R": 0.88 , 
        "Z_Vel_R": 0.00, 
        "destinationFileName_R": "PROC-TRAIN2-SIDESTEPS-R-SML-80BPM.xlsx" 
    },
]

def getClassificationSpeed(bpm):
    if(bpm < UPPER_BOUND_SLOW_BPM ):
        return 'SLOW'
    elif( bpm < UPPER_BOUND_MEDIUM_BPM):
        return 'AVERAGE'
    else:
        return 'FAST'

for fileConfig in FILES_ARRAY:
    file_path = SOURCE_FOLDER_PATH + fileConfig["fileName"]


    fileNameSplit = fileConfig["fileName"].split("-")
    getBPM = ''.join(filter(str.isdigit, fileNameSplit[-1]))
    getBPM = float(getBPM)

    classificationMotion = fileNameSplit[2]
    classificationMotionType = fileNameSplit[4]
    classificationMotionSpeed = getClassificationSpeed(getBPM)

    # Read the Excel file
    df = pd.read_csv(file_path)



    # Exclude rows where 'Notes1' is equal to 'CUTOFF'
    df = df[df['Notes1'] != 'CUTOFF']   

    # Filter the DataFrame for file A and B(STANDING_A and MOTION_A)
    file_a_df = df[df['Notes1'].isin(['STANDING_A', 'MOTION_A'])]
    file_b_df = df[df['Notes1'].isin(['STANDING_B', 'MOTION_B'])]

    

    file_a_df['L_Pitch_Delta'] = file_a_df['L_Pitch'].diff()
    file_a_df['L_Roll_Delta'] = file_a_df['L_Roll'].diff()
    file_a_df['R_Pitch_Delta'] = file_a_df['R_Pitch'].diff()
    file_a_df['R_Roll_Delta'] = file_a_df['R_Roll'].diff()

    file_b_df['L_Pitch_Delta'] = file_b_df['L_Pitch'].diff()
    file_b_df['L_Roll_Delta'] = file_b_df['L_Roll'].diff()
    file_b_df['R_Pitch_Delta'] = file_b_df['R_Pitch'].diff()
    file_b_df['R_Roll_Delta'] = file_b_df['R_Roll'].diff()

    # update values for file A
    file_a_df.loc[df['Notes1'] == 'STANDING_A', ['Notes1', 'X_Vel', 'Z_Vel']] = ['STANDING', 0, 0]
    file_a_df.loc[df['Notes1'] == 'STANDING_A', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['STAND', 'SML', 'SLOW']

    file_a_df.loc[df['Notes1'] == 'MOTION_A', ['X_Vel', 'Z_Vel']] = [fileConfig["X_Vel_L"], fileConfig["Z_Vel_L"]]   
    file_a_df.loc[df['Notes1'] == 'MOTION_A', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['L' + classificationMotion, classificationMotionType, classificationMotionSpeed] 


    # update values for file B
    file_b_df.loc[df['Notes1'] == 'STANDING_B', ['Notes1', 'X_Vel', 'Z_Vel']] = ['STANDING', 0, 0]
    file_b_df.loc[df['Notes1'] == 'STANDING_B', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['STAND', 'SML', 'SLOW']

    file_b_df.loc[df['Notes1'] == 'MOTION_B', ['Notes1','X_Vel', 'Z_Vel']] = [ 'MOTION_A', fileConfig["X_Vel_R"], fileConfig["Z_Vel_R"]]   
    file_b_df.loc[df['Notes1'] == 'MOTION_B', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['R' + classificationMotion, 'R' + classificationMotionType, classificationMotionSpeed] 


    # save the modified csv to a spreadsheet
    file_a_df.to_excel(DESTINATION_FOLDER_PATH + fileConfig["destinationFileName_L"], index=False)
    file_b_df.to_excel(DESTINATION_FOLDER_PATH + fileConfig["destinationFileName_R"], index=False)
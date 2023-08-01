import asyncio
import websockets
import json
import random
from datetime import datetime
import numpy as np 
import os 
import sys
from tensorflow.keras.models import load_model

# GET CURRENT DIRECTORY
CURRENT_DIRECTORY = os.getcwd()

# READ CONFIG FILE
config_file = open(CURRENT_DIRECTORY + '\\config\\config.json')
CONFIG_DATA = json.load(config_file)
config_file.close()

config_velocity_file = open(CURRENT_DIRECTORY + '\\config\\velocityConfig.json')
CONFIG_VELOCITY_DATA = json.load(config_velocity_file)
config_velocity_file.close()

############################################################
# IMPORT LOCAL OUT OF SCRIPT FUNCTIONS
############################################################

sys.path.append(CURRENT_DIRECTORY + '\\NeuralNetwork\\')
from ModelPredictor import ModelPredictor
sys.path.append(CURRENT_DIRECTORY + '\\config\\')
from config import normalize_sensor_data, calculateSensorDeltas, calculateAbsSensorDeltas, calculateMaxSensorData, calculateMinSensorData, count_sequences_above_threshold, count_sequences_below_threshold, prediction_class_label, processStepsMotionSpeed, prediction_class_label_binary, processLSideStepsMotionSpeed, processRLarSideStepsMotionSpeed

# ##############################################################
# IMPORT THE NUMBER OF PARAMETERS WE NEED
# ##############################################################

MAX_TIMESTEPS = CONFIG_DATA['WINDOW_SIZE']
NUMBER_OF_FEATURES = CONFIG_DATA["NUMBER_OF_FEATURES"]
ENABLE_CONSTANT_DELTA_SPEED = CONFIG_DATA["ENABLE_CONSTANT_DELTA_SPEED"]
MODEL_PATH = CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\model2.h5'

CLASSES_MOTION = CONFIG_DATA["CLASSES_MOTION"]
CLASSES_MOTIONTYPE = CONFIG_DATA["CLASSES_MOTIONTYPE"]
CLASSES_MOTIONSPEED = CONFIG_DATA["CLASSES_MOTIONSPEED"]
CLASSES_MOTIONSPEED_2 = CONFIG_DATA["CLASSES_MOTIONSPEED_2"]

LAR_STEPS_PITCH_ROTATION_THRESHOLD = CONFIG_DATA["LAR_STEPS_PITCH_ROTATION_THRESHOLD"]
SML_STEPS_PITCH_ROTATION_THRESHOLD = CONFIG_DATA["SML_STEPS_PITCH_ROTATION_THRESHOLD"]

SML_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD = CONFIG_DATA["SML_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD"]
SML_R_SIDESTEPS_ROLL_ROTATION_THRESHOLD = CONFIG_DATA["SML_R_SIDESTEPS_ROLL_ROTATION_THRESHOLD"]

LAR_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD = CONFIG_DATA["LAR_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD"]
LAR_R_SIDESTEPS_ROLL_ROTATION_THRESHOLD = CONFIG_DATA["LAR_R_SIDESTEPS_ROLL_ROTATION_THRESHOLD"]

############################################################
# IMPORT ALL OF THE MODELS WE NEED FOR OUR PREDICTION
############################################################

# LAYER 1
predict_motion = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motion-2.h5')

# LAYER 2
predict_motiontype_steps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motiontype-steps-2.h5')
predict_motiontype_lsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motiontype-lsidesteps-2.h5')
predict_motiontype_rsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motiontype-rsidesteps-2.h5')

# LAYER 3
predict_motionspeed_lar_steps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-lar-steps-2.h5')
predict_motionspeed_sml_steps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-sml-steps-2.h5')

predict_motionspeed_lar_lsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-lar-lsidesteps-2.h5')
predict_motionspeed_sml_lsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-sml-lsidesteps-2.h5')

predict_motionspeed_lar_rsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-lar-rsidesteps-2.h5')
predict_motionspeed_sml_rsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-sml-rsidesteps-2.h5')


########################################################################
# THIS WILL HANDLE THE MESSAGE RETURNED BY THE WEBSOCKET (AKA. THE GAME)
########################################################################
def process_request(message):
    motion_label = ""
    motiontype_label = ""
    motionspeed_label = ""
    motion_config = {}

    response = {
        'x_velocity': 0.000,
        'y_velocity': 0.000,
        'z_velocity': 0.000
    }    
    
    # Process the request and return the response
    sensor_data = json.loads(message)

    input_sensor_data = np.reshape(np.array(sensor_data), (MAX_TIMESTEPS + 1, NUMBER_OF_FEATURES))

    input_delta_data = calculateSensorDeltas(input_sensor_data)

    input_total_deltas = calculateAbsSensorDeltas(input_delta_data)
    input_total_deltas = np.reshape(input_total_deltas, (1, NUMBER_OF_FEATURES))

    motion_prediction = predict_motion.predict(input_total_deltas)
    motion_label = prediction_class_label(motion_prediction, CLASSES_MOTION)

    ##########################################
    # LOGIC IF MOTION IS STANDING
    ##########################################
    if(motion_label == 'STANDING'):
        motion_config = CONFIG_VELOCITY_DATA[motion_label]


    ##########################################
    # LOGIC IS MOTION IS STEPS
    ##########################################
    elif(motion_label == "STEPS"):
        max_sensor_data = calculateMaxSensorData(input_sensor_data)
        max_pitch_reading = np.max(max_sensor_data[:, [0, 2]], axis=1)

        motiontype_prediction = predict_motiontype_steps.predict(max_pitch_reading)
        motiontype_label = prediction_class_label_binary(motiontype_prediction, CLASSES_MOTIONTYPE)

        if(motiontype_label == "LAR"):
            process_motionspeed_inputs = processStepsMotionSpeed(input_sensor_data, input_total_deltas, LAR_STEPS_PITCH_ROTATION_THRESHOLD)

            motionspeed_prediction = predict_motionspeed_lar_steps.predict(process_motionspeed_inputs)
            motionspeed_label = prediction_class_label(motionspeed_prediction, CLASSES_MOTIONSPEED)


        elif(motiontype_label == "SML"):
            process_motionspeed_inputs = processStepsMotionSpeed(input_sensor_data, input_total_deltas, SML_STEPS_PITCH_ROTATION_THRESHOLD)

            motionspeed_prediction = predict_motionspeed_sml_steps.predict(process_motionspeed_inputs)
            motionspeed_label = prediction_class_label_binary(motionspeed_prediction, CLASSES_MOTIONSPEED_2)

        motion_config = CONFIG_VELOCITY_DATA[motion_label + '-' + motiontype_label + '-' + motionspeed_label]


    ##########################################
    # LOGIC IF MOTION IS LSIDESTEPS
    ##########################################
    elif(motion_label == "LSIDESTEPS"):
        max_sensor_data = calculateMaxSensorData(input_sensor_data)
        min_sensor_data = calculateMinSensorData(input_sensor_data)

        input_minmax = np.column_stack((max_sensor_data, min_sensor_data))
        process_motiontype_inputs = input_minmax[:, [1, 5]]

        motiontype_prediction = predict_motiontype_lsidesteps.predict(process_motiontype_inputs)
        motiontype_label = prediction_class_label_binary(motiontype_prediction, CLASSES_MOTIONTYPE)

        if(motiontype_label == "LAR"):
            process_motionspeed_inputs = processLSideStepsMotionSpeed(input_sensor_data, input_total_deltas, LAR_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD)

            motionspeed_prediction = predict_motionspeed_lar_lsidesteps.predict(process_motionspeed_inputs)
            motionspeed_label = prediction_class_label_binary(motionspeed_prediction, CLASSES_MOTIONSPEED_2)

        elif(motiontype_label == "SML"):
            process_motionspeed_inputs = processLSideStepsMotionSpeed(input_sensor_data, input_total_deltas, SML_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD)

            motionspeed_prediction = predict_motionspeed_sml_lsidesteps.predict(process_motionspeed_inputs)
            motionspeed_label = prediction_class_label_binary(motionspeed_prediction, CLASSES_MOTIONSPEED_2)
    
        motion_config = CONFIG_VELOCITY_DATA[motion_label + '-' + motiontype_label + '-' + motionspeed_label]


    ##########################################
    # LOGIC IF MOTION IS RSIDESTEPS
    ##########################################
    elif(motion_label == "RSIDESTEPS"):
        max_sensor_data = calculateMaxSensorData(input_sensor_data)
        min_sensor_data = calculateMinSensorData(input_sensor_data)

        input_minmax = np.column_stack((max_sensor_data, min_sensor_data))
        process_motiontype_inputs = input_minmax[:, [3, 7]]

        motiontype_prediction = predict_motiontype_rsidesteps.predict(process_motiontype_inputs)
        motiontype_label = prediction_class_label_binary(motiontype_prediction, CLASSES_MOTIONTYPE)

        if(motiontype_label == "LAR"):
            process_motionspeed_inputs = processRLarSideStepsMotionSpeed(input_sensor_data, input_total_deltas, LAR_L_SIDESTEPS_ROLL_ROTATION_THRESHOLD)

            motionspeed_prediction = predict_motionspeed_lar_lsidesteps.predict(process_motionspeed_inputs)
            motionspeed_label = prediction_class_label_binary(motionspeed_prediction, CLASSES_MOTIONSPEED_2)

        elif(motiontype_label == "SML"):
            motionspeed_label = "FAST"
            print("TO DO")


        motion_config = CONFIG_VELOCITY_DATA[motion_label + '-' + motiontype_label + '-' + motionspeed_label]


    #######################
    # ASSIGN VELOCITIES 
    #######################
    if(ENABLE_CONSTANT_DELTA_SPEED == True):
        total_pitch_deltas = np.sum(input_total_deltas[:, [0,2]])
        total_lroll_deltas = np.sum(input_total_deltas[:,1])
        total_rroll_deltas = np.sum(input_total_deltas[:,3])

        if(motion_label == "STEPS"):
            response['z_velocity'] = motion_config['z_velocity'] + total_pitch_deltas*motion_config['addConstant']
        elif(motion_label == "LSIDESTEPS"):
            response['x_velocity'] = motion_config['x_velocity'] + total_lroll_deltas*motion_config['addConstant']
        elif(motion_label == "RSIDESTEPS"):
            response['x_velocity'] = motion_config['x_velocity'] + total_rroll_deltas*motion_config['addConstant']

    else:   
        response['x_velocity'] = motion_config['x_velocity']
        response['z_velocity'] = motion_config['z_velocity']

    print(motion_label + '-' + motiontype_label + '-' + motionspeed_label)
    print(response)

    return response


#######################################################################
# CREATE WEBSOCKET SERVER ON PORT 3003
# THIS SERVER IS HOW OUR GAME WILL COMMUNICATE TO OUR PYTHON SCRIPTs
########################################################################
async def handle_websocket(websocket, path):
    print(str(datetime.now()) + ": Client connected")


    await websocket.send("You are now connected via WebSocket")
    try:
        while True:
            # RECIEVE MESSAGE FROM CLIENT
            message = await websocket.recv()

            # PROCESS AND CREATE RESPONSE FOR CLIENT
            response = process_request(message)
            response_json = json.dumps(response)

            # SEND RESPONSE TO CLIENT
            await websocket.send(response_json)


    except websockets.exceptions.ConnectionClosed:
        print(str(datetime.now())  + ": Client disconnected")

if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket, "localhost", 3003)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
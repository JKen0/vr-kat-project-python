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

#
# IMPORT LOCAL OUT OF SCRIPT FUNCTIONS
#
sys.path.append(CURRENT_DIRECTORY + '\\NeuralNetwork\\')
from ModelPredictor import ModelPredictor
sys.path.append(CURRENT_DIRECTORY + '\\config\\')
from config import normalize_sensor_data, calculateSensorDeltas, calculateAbsSensorDeltas, calculateMaxSensorData, calculateMinSensorData, count_sequences_above_threshold, count_sequences_below_threshold, prediction_class_label


# 
# IMPORT THE NUMBER OF PARAMETERS WE NEED
# 
MAX_TIMESTEPS = CONFIG_DATA['WINDOW_SIZE']
NUMBER_OF_FEATURES = CONFIG_DATA["NUMBER_OF_FEATURES"]
MODEL_PATH = CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\model2.h5'

CLASSES_MOTION = CONFIG_DATA["CLASSES_MOTION"]
CLASSES_MOTIONTYPE = CONFIG_DATA["CLASSES_MOTIONTYPE"]
CLASSES_MOTIONSPEED = CONFIG_DATA["CLASSES_MOTIONSPEED"]
CLASSES_MOTIONSPEED_2 = CONFIG_DATA["CLASSES_MOTIONSPEED_2"]

#
# IMPORT ALL OF THE MODELS WE NEED FOR OUR PREDICTION
#
# LAYER 1
predict_motion = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motion-2.h5')

# LAYER 2
predict_motiontype_steps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motiontype-steps-2.h5')
predict_motiontype_lsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motiontype-lsidesteps-2.h5')
predict_motion_rsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motiontype-rsidesteps-2.h5')

# LAYER 3
predict_motiontype_lar_steps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-lar-steps-2.h5')
predict_motiontype_sml_steps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-sml-steps-2.h5')

#predict_motiontype_lar_lsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-lar-lsidesteps-2.h5')
#predict_motiontype_sml_lsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-sml-lsidesteps-2.h5')

predict_motiontype_lar_rsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-lar-rsidesteps-2.h5')
predict_motiontype_sml_rsidesteps = load_model(CURRENT_DIRECTORY + '\\NeuralNetwork\\models\\standard-backprop-motionspeed-sml-rsidesteps-2.h5')



# THIS WILL HANDLE THE MESSAGE RETURNED BY THE WEBSOCKET (AKA. THE GAME)
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

    #input_sensor_data = np.reshape(np.array(sensor_data), (MAX_TIMESTEPS + 1, NUMBER_OF_FEATURES))

    #input_delta_data = calculateSensorDeltas(input_sensor_data)

    #input_total_deltas = calculateAbsSensorDeltas(input_delta_data)
    #input_total_deltas = np.reshape(input_total_deltas, (1, NUMBER_OF_FEATURES))

    input_total_deltas = np.array([0, 0, 0, 0])
    input_total_deltas = np.reshape(input_total_deltas, (1, 4))

    motion_prediction = predict_motion.predict(input_total_deltas)
    motion_label = prediction_class_label(motion_prediction, CLASSES_MOTION)

    if(motion_label == 'STANDING'):
        motion_config = CONFIG_VELOCITY_DATA[motion_label]

    #elif(motion_label == "STEPS"):

    #elif(motion_label == "LSIDESTEPS"):
    
    #elif(motion_label == "RSIDESTEPS"):

    print(motion_label)

    response['x_velocity'] == motion_config['x_velocity']
    response['z_velocity'] == motion_config['z_velocity']

    return response

print(process_request("[]"))


# CREATE WEBSOCKET SERVER ON PORT 3003
# THIS SERVER IS HOW OUR GAME WILL COMMUNICATE TO OUR PYTHON SCRIPTs
async def handle_websocket(websocket, path):
    model_predictor = ModelPredictor(MODEL_PATH)
    print('Socket is now using model: ', MODEL_PATH)
    
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
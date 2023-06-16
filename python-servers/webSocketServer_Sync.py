import asyncio
import websockets
import json
import random
from datetime import datetime
import numpy as np 

import sys
sys.path.append('C:/Dev/vr-kat-project-python-2/NeuralNetwork/')

from ModelPredictor import ModelPredictor


MAX_TIMESTEPS = 10
NUMBER_OF_FEATURES = 4
MODEL_PATH = 'test-model.h5'

def update_previous_sensor_data(new_sensor_data, previous_sensor_data):

    # Append the new sensor data to the list
    previous_sensor_data.append(new_sensor_data)

        


def process_request(model_predictor, message, previous_sensor_data):
    # Process the request and return the response
    sensor_data = json.loads(message)

    L_Pitch_Data = sensor_data["L_Pitch"]
    L_Roll_Data = sensor_data["L_Roll"]
    R_Pitch_Data = sensor_data["R_Pitch"]
    R_Roll_Data = sensor_data["R_Roll"]

    # FEED THE SENSORS TO OUR NEURAL NETWORK
    new_sensor_data = np.array([L_Pitch_Data, L_Roll_Data, R_Pitch_Data, R_Roll_Data])

    #print(new_sensor_data)

    # Append the new sensor data to the list
    previous_sensor_data.append(new_sensor_data)

    # Keep only the most recent 'max_timesteps' entries
    if len(previous_sensor_data) >= MAX_TIMESTEPS:
        previous_sensor_data = previous_sensor_data[-MAX_TIMESTEPS:]

    # IN RETURN WE WILL GET A VECT REPRESENTING VELOCITY
    response = {
        'x_velocity': 0.000,
        'y_velocity': 0.000,
        'z_velocity': 0.000
    }

    if(len(previous_sensor_data) == MAX_TIMESTEPS):
        reshape_input_data = np.reshape(previous_sensor_data, (1, MAX_TIMESTEPS, NUMBER_OF_FEATURES))
        reshape_input_data = reshape_input_data[:][::-1]

        

        #print(reshape_input_data)


        velocity_prediction = model_predictor.predict(reshape_input_data)
        response['x_velocity'] = str(round(velocity_prediction[0][0], 3))
        response['z_velocity'] = str(round(velocity_prediction[0][1], 3))

    return response

async def handle_websocket(websocket, path):
    PREVIOUS_SENSOR_DATA = []
    ITERATION = 0
    
    model_predictor = ModelPredictor(MODEL_PATH)
    print('Socket is now using model: ', MODEL_PATH)

    
    print(str(datetime.now()) + ": Client connected")
    await websocket.send("You are now connected via WebSocket")

    try:
        while True:
            #print(len(PREVIOUS_SENSOR_DATA))

            # RECIEVE MESSAGE FROM CLIENT
            message = await websocket.recv()


            # PROCESS AND CREATE RESPONSE FOR CLIENT
            response = process_request(model_predictor, message, PREVIOUS_SENSOR_DATA)
            response_json = json.dumps(response)

            # SEND RESPONSE TO CLIENT
            await websocket.send(response_json)
    except websockets.exceptions.ConnectionClosed:
        print(str(datetime.now())  + ": Client disconnected")

if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket, "localhost", 3003)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
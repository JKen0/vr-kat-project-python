import asyncio
import websockets
import json
import random
from datetime import datetime
import numpy as np 
import os 

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()
# Get the parent directory
PARENT_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)

import sys

sys.path.append(PARENT_DIRECTORY + '\\NeuralNetwork\\')

from ModelPredictor import ModelPredictor

# IMPORTANT PARAMETERS FOR THE MODEL
MAX_TIMESTEPS = 10
NUMBER_OF_FEATURES = 4
MODEL_PATH = PARENT_DIRECTORY + '\\NeuralNetwork\\models\\model2.h5'

        
# THIS WILL  HANDLE THE MESSAGE RETURNED BY THE WEBSOCKET (AKA. THE GAME)
def process_request(model_predictor, message):
    # Process the request and return the response
    sensor_data = json.loads(message)

    input_data_reshape = np.reshape(np.array(sensor_data), (1, MAX_TIMESTEPS, NUMBER_OF_FEATURES))

    # IN RETURN WE WILL GET A VECT REPRESENTING VELOCITY
    response = {
        'x_velocity': 0.000,
        'y_velocity': 0.000,
        'z_velocity': 0.000
    }

    velocity_prediction = model_predictor.predict(input_data_reshape)

    response['x_velocity'] = str(round(-1*velocity_prediction[0][0] + velocity_prediction[0][1], 3))
    response['z_velocity'] = str(round(velocity_prediction[0][2], 3))

    return response



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
            response = process_request(model_predictor, message)
            response_json = json.dumps(response)

            # SEND RESPONSE TO CLIENT
            await websocket.send(response_json)


    except websockets.exceptions.ConnectionClosed:
        print(str(datetime.now())  + ": Client disconnected")

if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket, "localhost", 3003)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
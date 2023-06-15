import asyncio
import websockets
import json
import random
from datetime import datetime
import numpy as np 
from NeuralNetwork.ModelPredictor import ModelPredictor


MAX_TIMESTEPS = 10
PREVIOUS_SENSOR_DATA = []
MODEL_PATH = 'test-model.h5'

def update_previous_sensor_data(new_sensor_data):
    # Append the new sensor data to the list
    previous_sensor_data.append(new_sensor_data)
    
    # Keep only the most recent 'max_timesteps' entries
    if len(previous_sensor_data) > MAX_TIMESTEPS:
        previous_sensor_data = previous_sensor_data[-PREVIOUS_SENSOR_DATA:]


def process_request(model_predictor, message):
    # Process the request and return the response
    sensor_data = json.loads(message)

    L_Pitch_Data = sensor_data["L_Pitch"]
    L_Roll_Data = sensor_data["L_Roll"]
    R_Pitch_Data = sensor_data["R_Pitch"]
    R_Roll_Data = sensor_data["R_Roll"]

    # FEED THE SENSORS TO OUR NEURAL NETWORK
    new_sensor_data = np.array([L_Pitch_Data, L_Roll_Data, R_Pitch_Data, R_Roll_Data])
    update_previous_sensor_data(new_sensor_data)


    # IN RETURN WE WILL GET A VECT REPRESENTING VELOCITY
    response = {
        'x_velocity': 0.000,
        'y_velocity': 0.000,
        'z_velocity': 0.000
    }

    if(len(PREVIOUS_SENSOR_DATA) == MAX_TIMESTEPS):
        velocity_prediction = model_predictor.predict(PREVIOUS_SENSOR_DATA)
        response['x_velocity'] = velocity_prediction[0]
        response['z_velocity'] = velocity_prediction[1]

    return response

async def handle_websocket(websocket, path):
    model_predictor = ModelPredictor(MODEL_PATH)
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
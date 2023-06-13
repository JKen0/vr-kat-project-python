import asyncio
import websockets
import json
import random
from datetime import datetime


def process_request(message):
    # Process the request and return the response
    sensor_data = json.loads(message)

    L_Pitch_Data = sensor_data["L_Pitch"]
    L_Roll_Data = sensor_data["L_Roll"]
    R_Pitch_Data = sensor_data["R_Pitch"]
    R_Roll_Data = sensor_data["R_Roll"]

    # FEED THE SENSORS TO OUR NEURAL NETWORK
    # TO DO IN THE FUTURE

    # IN RETURN WE WILL GET A VECT REPRESENTING VELOCITY
    response = {
        'x_velocity': random.randrange(20),
        'y_velocity': random.randrange(20),
        'z_velocity': random.randrange(20)
    }

    return response

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
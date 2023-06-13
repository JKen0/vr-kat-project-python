import websockets
import asyncio

async def handle_websocket(websocket, path):
    print("Client connected")
    await websocket.send("You are now connected via WebSocket")

    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            response = process_request(message)
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

def process_request(message):
    # Assuming the message is a comma-separated string of four parameters
    params = message.split(',')
    if len(params) != 4:
        return "Invalid request. Expected four parameters."

    # Process the parameters and return the response
    # Modify this part to perform your desired logic based on the parameters
    response = f"Request received. Parameters: {params}"
    return response

if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket, "localhost", 3002)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
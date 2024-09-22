import asyncio
import websockets

async def receive_data(websocket):
    async for message in websocket:
        number = int.from_bytes(message, byteorder='little', signed=False)
        print(f"Received number: {number}")

async def main():
    async with websockets.connect('ws://localhost:9001') as websocket:
        print("Connected to server")
        asyncio.create_task(receive_data(websocket))

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

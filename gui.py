import asyncio
import websockets
import bokeh.plotting as bpl
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show

source = ColumnDataSource(data=dict(x=[0], y=[0]))

async def receive_data(websocket):
    async for message in websocket:
        number = int.from_bytes(message, byteorder='big', signed=False)
        new_data = dict(x=[source.data['x'][0] + 65535], y=[number])
        source.stream(new_data)

async def main():
    async with websockets.connect('ws://localhost:9001') as websocket:
        print("Connected to server")
        asyncio.create_task(receive_data(websocket))

        # Bokeh setup
        fig = figure(title="Random Numbers", x_axis_label="Time", y_axis_label="Value")
        line = fig.line(x='x', y='y', source=source)

        show(fig, websocket_origin="localhost:9001")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

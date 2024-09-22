from bokeh.models import DataSource
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
import asyncio
from tornado.ioloop import IOLoop
from bokeh.document import Document
import websockets

class RandDocument():
    doc: Document | None = None
    textDataSource: DataSource | None = None

    def __init__(self):
        io_loop = IOLoop.current()
        self.server = Server({'/': self.bkapp}, io_loop=io_loop, port=5006)
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        
    def bkapp(self, doc):
        self.doc = doc

        p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
        p.outline_line_color = None
        p.grid.grid_line_color = None
        p.xaxis.visible = False
        p.yaxis.visible = False
        # add a text renderer to the plot (no data yet)
        r = p.text(x=[50], y=[50], text=["?"], text_color=["#000000"], text_font_size="64px",
                text_baseline="middle", text_align="center")
        self.textDataSource = r.data_source
        doc.add_root(p)

    async def receive_new_numbers(self, websocket):
        async for message in websocket:
            n = int.from_bytes(message, byteorder='little', signed=False)
            print(f"Received number: {n}")
            self.doc.add_next_tick_callback(lambda: self.textDataSource.data.update({"text": [str(n)]}))

async def main():
    rd = RandDocument()
    async with websockets.connect('ws://localhost:9001') as websocket:
        print("Connected to server")
        asyncio.create_task(rd.receive_new_numbers(websocket))

        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
import asyncio
from tornado.ioloop import IOLoop
from bokeh.document import Document


df = sea_surface_temperature.copy()
source = ColumnDataSource(data=df)
d: Document | None = None
i = 0
def bkapp(doc):

    global d
    d = doc

    plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)
        
    doc.add_root(plot)

async def updateDocData():
    print("Periodic callback called")
    global i
    if i == 0:
        data = df
    else:
        data = df.rolling(f"{i}D").mean()
    source.data = ColumnDataSource.from_df(data)
    i += 1

async def my_loop():
    for i in range(10):
        await asyncio.sleep(1)
        print(f"queueing callback for i={i}")
        global d
        if d:
            d.add_next_tick_callback(updateDocData)

async def main():
    io_loop = IOLoop.current()
    server = Server({'/': bkapp}, io_loop=io_loop, port=5006)
    server.start()
    server.io_loop.add_callback(server.show, "/")

    my_loop_task = asyncio.create_task(my_loop())

    await my_loop_task

if __name__ == '__main__':
    asyncio.run(main())
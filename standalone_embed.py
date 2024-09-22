from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from time import sleep
import threading

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


server = Server({'/': bkapp})
server.start()
server.io_loop.add_callback(server.show, "/")

def updateDocData():
    print("Periodic callback called")
    global i
    if i == 0:
        data = df
    else:
        data = df.rolling(f"{i}D").mean()
    source.data = ColumnDataSource.from_df(data)
    i += 1

def my_loop():
    for i in range(10):
        sleep(1)
        print(f"queueing callback for i={i}")
        global d
        d.add_next_tick_callback(updateDocData)

if __name__ == '__main__':

    # Create and start a thread for the io_loop
    io_loop_thread = threading.Thread(target=server.io_loop.start)
    io_loop_thread.start()

    # Run the other loop in the main thread
    my_loop()
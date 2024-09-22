from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
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
        
    def callback(attr, old, new):
        print(f"attr: {attr}, old: {old}, new: {new}")
        if new == 0:
            data = df
        else:
            data = df.rolling(f"{new}D").mean()
        source.data = ColumnDataSource.from_df(data)

    def cb2():
        print("Periodic callback called")
        global i
        callback("Periodic", 0, i)
        i += 1
    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)
    #doc.add_periodic_callback(cb2, 1000)
    doc.add_root(column(slider, plot))


server = Server({'/': bkapp})
server.start()


def cbnew(attr, old, new):
    #session = server.get_sessions('/')[0]
    #add_next_tick_callback
    print(f"attr: {attr}, old: {old}, new: {new}")
    if new == 0:
        data = df
    else:
        data = df.rolling(f"{new}D").mean()
    source.data = ColumnDataSource.from_df(data)

def cbnew2():
    print("Periodic callback called")
    global i
    cbnew("Periodic", 0, i)
    i += 1

def run_io_loop():
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

def my_loop():
    for i in range(10):
        sleep(1)
        print(f"queueing callback for i={i}")
        global d
        d.add_next_tick_callback(cbnew2)

if __name__ == '__main__':

    # Create and start a thread for the io_loop
    io_loop_thread = threading.Thread(target=run_io_loop)
    io_loop_thread.start()

    # Run the other loop in the main thread
    my_loop()
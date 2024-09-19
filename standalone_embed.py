from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from time import sleep

df = sea_surface_temperature.copy()
source = ColumnDataSource(data=df)

def bkapp(doc):


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

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))


# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.
server = Server({'/': bkapp}, num_procs=1)
server.start()


def cbnew(attr, old, new):
    print(f"attr: {attr}, old: {old}, new: {new}")
    if new == 0:
        data = df
    else:
        data = df.rolling(f"{new}D").mean()
    source.data = ColumnDataSource.from_df(data)

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")

    server.io_loop.start()

    for i in range(10):
        print(i)
        sleep(2)
        server.io_loop.add_callback(cbnew, 'derp', i, i+1)
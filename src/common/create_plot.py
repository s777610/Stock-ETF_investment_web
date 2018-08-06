
from pandas_datareader import data
import fix_yahoo_finance as yf
import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN  # content delivery network
from bokeh.models import HoverTool, ColumnDataSource


# get new colums, Status
def inc_dec(close, open):
    if close > open:
        value = "Increase"
    elif close < open:
        value = "Decrease"
    else:
        value = "Equal"
    return value


def create_plot(name, ticker):
    # Using yahoo API
    yf.pdr_override()

    # from 3 months ago to now
    start = datetime.datetime.now() - datetime.timedelta(days=180)
    end = datetime.datetime.now()
    df = data.get_data_yahoo(ticker, start=start, end=end)

    # create new columns in order to plot
    df["Status"] = [inc_dec(close, open) for close, open in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p.title.text = f"{name} Candlestick Chart"
    p.grid.grid_line_alpha = 0.3  # alpha is level of transparent

    hours_12 = 12 * 60 * 60 * 1000  # millisconds

    # 4 parameter, x value of high point, y value of high point, x value of low point, y value of low point
    p.segment(df.index, df.High, df.index, df.Low, color="Black", name='segment')

    # for hover
    col_data_src1 = ColumnDataSource(df[df.Status == 'Increase'])
    col_data_src2 = ColumnDataSource(df[df.Status == 'Decrease'])

    # 4 parameter, x-axis(datetime), y-axis, width(milliseconds in this case), height
    p.rect('Date', 'Middle', hours_12,
           'Height', fill_color='green', line_color='black',
           source=col_data_src1, name='Increase')

    p.rect('Date', 'Middle', hours_12,
           'Height', fill_color='red', line_color='black',
           source=col_data_src2, name='Decrease')

    hover = HoverTool(names=["Increase", "Decrease"], tooltips=[('Open', '@Open'), ('Close', '@Close'), ('High', '@High'), ('Low', '@Low')])
    p.add_tools(hover)

    current_price = df.iloc[-1]["Close"].round(2)

    today_status = df.iloc[-1]["Status"]
    if today_status == "Increase":
        name_color = "green"
    else:
        name_color = "red"

    time_string = df.index[-1].strftime('%m/%d/%Y')
    last_updated = time_string

    # the source code of JS and html, which is tuple(len=2)
    # script1 is JS, div1 is html, both type are string
    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]  # js_files is a list of bokeh source code
    cdn_css = CDN.css_files[0]  # css_files is a list of bokeh source code

    return name, script1, div1, cdn_css, cdn_js, current_price, name_color, today_status, last_updated

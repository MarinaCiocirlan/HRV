#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 16:01:39 2018

@author: marina
"""

import json
import urllib.request

from pprint import pprint
from operator import itemgetter
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette

# read input data
url = urllib.request.urlopen("http://206.189.54.146/interval")
response = url.read()
data = json.loads(response)
#pprint(data)

# list of figures
figures = []

# output to static HTML file
output_file("lines.html")

# bokeh tools
tools_to_show = 'hover, box_zoom, pan, save, reset, wheel_zoom'

# printare sesiuni
for dIndex, dValue in enumerate(data):
    
    tmp_data = data[dValue]
    if len(tmp_data) == 0:
        continue
    # order dictionary by timestamp
    tmp_data = sorted(tmp_data, key=itemgetter(0))
    
    # define figure
    p = figure(plot_width=1500, plot_height=800, tools=tools_to_show,
               title="HRV evolution", x_axis_label='timestamp', y_axis_label='HRV')
    
    # extract RTC and HRV
    x = [i[0] for i in tmp_data] # RTC
    #x = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(tmp_x))) for tmp_x in x]
    y = [i[1] for i in tmp_data] # HRV
    
    source = ColumnDataSource(data={
                'x': x, 
                'y': y
            })
    p.line('x', 'y', source=source, legend=dValue, line_width=4, color=palette[dIndex % 5])

    figures.append(p)

# show the results
show(column(figures))
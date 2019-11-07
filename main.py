from bokeh.io import curdoc
from bokeh.layouts import widgetbox, column, row
from bokeh.layouts import layout as lyt
from bokeh.models.widgets import TextInput,  Div
from bokeh.events import ButtonClick
from bokeh.models import Button
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker,
                          Slider, Label, CategoricalColorMapper, Span,
                          Whisker)
from bokeh.plotting import figure
from bokeh.models.widgets import Tabs, Panel
import numpy as np
from datamodel import datahandler
import pandas_bokeh

data_model = datahandler.DataModel()
lucknum = data_model.return_luck()
layout2 = lyt()

### TAB 1
pre = Div(text="", width=100, height=300, style={'font-size': '600%', 'color': 'blue'})
country_text = Div(text='', width=1000, height=50, style={'font-size': '200%', 'color': 'blue'})
chance_text = Div(text='', width=1000, height=20, style={'font-size': '100%', 'color': 'blue'})


def luck(event):
    data_model.change_luck()
    lucknum = data_model.return_luck()
    pre.text = '<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}</b>'.format(lucknum)
    layout2 = tab2_plotting()

    tabs.tabs = [Panel(child=layout1, title='aaaa'),
                 Panel(child=layout2, title='bbbb')]


def byear(attrname, old, new):
    year = text_input.value
    data_model.change_byear(year)
    c, chance = data_model.draw_country(year)
    country_text.text = '<b>{}</b>'.format(c)
    chance_text.text = '<b>you had {}% chance to be born here</b>'.format(chance)
    world = data_model.return_world()
    mapplot = world[world.name == c].plot_bokeh(
        figsize=(900, 600),
        simplify_shapes=5000,
        xlim=(-170, 170),
        ylim=(-40, 70),
        show_colorbar=False,
        colormap=['green'],
        tile_provider='CARTODBPOSITRON',
        show_figure=False,
        toolbar_location=None,
        xlabel=None,
        ylabel=None,
        legend=False)
    mapplot.axis.visible = False
    mapplot.min_border_left = 0
    mapplot.min_border_right = 0
    mapplot.min_border_bottom = 0
    mapplot.min_border_top = 0
    layout1.children = [row(
        column(widgetbox(text_input), widgetbox(country_text), widgetbox(chance_text), mapplot),
        column(widgetbox(button),widgetbox(pre))
    )]
    layout2 = tab2_plotting()

    tabs.tabs = [Panel(child=layout1, title='aaaa'),
                 Panel(child=layout2, title='bbbb')]


### WIDGETS
button = Button(label='Get my luck number!')
button.on_event(ButtonClick, luck)

text_input = TextInput(value="Birth Year", title="")

layout1 = lyt(children=[row(
    column(widgetbox(text_input))
)], sizing_mode='scale_both')

text_input.on_change('value', byear)


tabs = Tabs(tabs=[Panel(child=layout1, title='aaaa')])


### TAB 2
def tab2_plotting():
    datasource = data_model.return_country_data()
    byear = data_model.return_byear()

    source = ColumnDataSource(data=datasource[int(byear)])
    
    plot = figure(y_range=(-1, 10), x_range=(100, 0), title='', plot_height=270, plot_width=600)

    label = Label(x=100, y=9, text='When born - ' + str(data_model.return_byear()),
                  text_font_size='20pt',
                  text_baseline='middle',
                  text_color='#827262',
                  text_align='left',
                  text_font_style='normal',
                  text_font='Gilbert')
    plot.add_layout(label)

    label2 = Label(x=100, y=5, text='When 20 years old - ' + str(int(data_model.return_byear())+20),
                   text_font_size='20pt',
                   text_color='#827262',
                   text_align='left',
                   text_font_style='normal',
                   text_baseline='middle',
                   text_font='Frontage Outline')
    plot.add_layout(label2)

    label3 = Label(x=data_model.return_luck(), y=9.5, text='Luck limit',
                   text_font_size='20pt',
                   text_color='#827262',
                   text_align='center',
                   text_font_style='normal',
                   text_baseline='middle',
                   text_font='Frontage Outline')
    plot.add_layout(label3)

    for k, v in data_model.return_labelsmap().items():
        plot.add_layout(Label(x=2, y=v, text=k,
                              text_font_size='40pt',
                              text_color='#eeeeee',
                              text_align='right',
                              text_baseline='middle',
                              text_font_style='bold',
                              text_font='Gilbert'))

    plot.rect(
        x='valper2',
        y='yaxis',
        source=source,
        fill_color='color',
        fill_alpha=0.8,
        line_color='color',
        line_width=5,
        line_cap='round',
        width='val',
        height=0.8
    )
    plot.add_layout(Whisker(base= data_model.return_luck(), lower=-1, upper=9,
                            line_width=3, line_color='#ACCD33', line_dash='dashed',
                            upper_head=None, lower_head=None))

    plot.axis.visible = False
    plot.min_border_left = 0
    plot.min_border_right = 0
    plot.min_border_bottom = 0
    plot.min_border_top = 0
    plot.background_fill_color = "#D5DADD"
    plot.toolbar.logo = None
    plot.toolbar_location = None

    def slider_update(attrname, old, new):
        year = slider.value
        label.text = 'When born - ' + str(year)
        label2.text = 'When 20 years old - ' + str(year+20)
        source.data = datasource[year]

    slider = Slider(start=1960, end=2015, value=int(data_model.return_byear()), step=1, title="Year")
    slider.on_change('value', slider_update)

    layout2 = lyt([
        [plot],
        [slider],
    ], sizing_mode='scale_width')
    return layout2


curdoc().add_root(tabs)
curdoc().title = "Gapminder"

import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show, output_notebook
from bokeh.models import CustomJS
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row, column
from bokeh.palettes import Category20
from bokeh.models.annotations import Title, Legend
from bokeh.models import LinearAxis, Range1d
Category10 = Category20[14]
from bokeh.plotting import reset_output
reset_output()

bv1 = pd.read_csv('datasets/bv1_sensors_rus_v3.csv')
bv2 = pd.read_csv('datasets/bv2_sensors_rus_v4.csv')

bv1['время формирования точки на БВ'] = pd.to_datetime(bv1['время формирования точки на БВ'])
bv1['время прихода точки на сервере'] = pd.to_datetime(bv1['время прихода точки на сервере'])

bv2['время формирования точки на БВ'] = pd.to_datetime(bv2['время формирования точки на БВ'])
bv2['время прихода точки на сервере'] = pd.to_datetime(bv2['время прихода точки на сервере'])

df1 = bv1[(bv1['Секция №1 Температура НП, t°'] < bv1['Секция №1 Температура НП, t°'].quantile(.96))
    & (bv1['Секция №3 Температура НП, t°'] < bv1['Секция №3 Температура НП, t°'].quantile(.83))]

df2 = bv2[(bv2['Секция №1 Температура НП, t°'] < bv2['Секция №1 Температура НП, t°'].quantile(.99))
    & (bv2['Секция №3 Температура НП, t°'] < bv2['Секция №3 Температура НП, t°'].quantile(.92))]

df1['время формирования точки на БВ'] = pd.to_datetime(df1['время формирования точки на БВ'], format='%d/%m/%Y')
df2['время формирования точки на БВ'] = pd.to_datetime(df2['время формирования точки на БВ'], format='%d/%m/%Y')

p1 = figure(x_axis_type='datetime', sizing_mode='scale_both')
p2 = figure(x_axis_type='datetime', sizing_mode='scale_both')
# p1.extra_y_ranges = {"binary": Range1d(start=-2, end=2)}
aline = p1.circle(df1['время формирования точки на БВ'], df1['Секция №1 Температура НП, t°'], line_width=2, color=Category10[0])
bline = p1.circle(df1['время формирования точки на БВ'], df1['Секция №3 Температура НП, t°'], line_width=2, color=Category10[4])

cline = p2.circle(df2['время формирования точки на БВ'], df2['Секция №1 Температура НП, t°'], line_width=2, color=Category10[2])
dline = p2.circle(df2['время формирования точки на БВ'], df2['Секция №3 Температура НП, t°'], line_width=2, color=Category10[6])

# p2 = figure(x_axis_type='datetime', plot_width=10000)
# eline = p1.circle(df['время прихода точки на сервере'], df['Скорость'], line_width=2, color=Viridis6[5])

p1.yaxis.axis_label = 'Ось 1'
p1.xaxis.axis_label = 'временная ось 1'
p2.yaxis.axis_label = 'Ось 2'
p2.xaxis.axis_label = 'временная ось 2'
# p2.yaxis.axis_label = 'Скорость'
# p2.xaxis.axis_label = 'время формирования точки на БВ'

legend1 = Legend(items=[
    ('Параметр 1', [aline]),
    ('Параметр 2', [bline]),
], location=(0, 250))

legend2 = Legend(items=[
    ('Параметр 3', [cline]),
    ('Параметр 4', [dline]),
], location=(0, 250))

t1 = Title()
t1.text = 'BOKEH_EXAMPLE_1_EMOTIONS'
p1.title = t1

t2 = Title()
t2.text = 'BOKEH_EXAMPLE_2_EMOTIONS'
p2.title = t2
# p2.title = t
p1.add_layout(legend1, 'left')
p2.add_layout(legend2, 'left')
# p2.add_layout(legend, 'left')
checkboxes1 = CheckboxGroup(labels=list(['Параметр 1', 'Параметр 2']),
                           active=[0, 1])
checkboxes2 = CheckboxGroup(labels=list(['Параметр 3', 'Параметр 4']),
                           active=[0, 1])


callback1 = CustomJS(code="""aline.visible = false; // aline and etc.. are 
                             bline.visible = false; // passed in from args
        
                            // cb_obj is injected in thanks to the callback
                             if (cb_obj.active.includes(0)){aline.visible = true;} 
                                // 0 index box is aline
                             if (cb_obj.active.includes(1)){bline.visible = true;} 
                                // 1 index box is bline
                            """,
                            args={'aline': aline, 'bline': bline})

callback2 = CustomJS(code="""cline.visible = false; // aline and etc.. are 
                             dline.visible = false; // passed in from args
        
                            // cb_obj is injected in thanks to the callback
                             if (cb_obj.active.includes(0)){cline.visible = true;} 
                                // 0 index box is aline
                             if (cb_obj.active.includes(1)){dline.visible = true;} 
                                // 1 index box is bline
                            """,
                            args={'cline': cline, 'dline': dline})


checkboxes1.js_on_click(callback1)
checkboxes2.js_on_click(callback2)

layout1 = row(p1, checkboxes1)
layout2 = row(p2, checkboxes2)
layout = column(layout1, layout2)
# output_file('BV2_DUT_sensors_134_sections.html')
# show(column(p1, p2, checkboxes))
curdoc().add_root(layout)
curdoc().title="BOKEH_EXAMPLE_EMOTIONS"

show(layout)
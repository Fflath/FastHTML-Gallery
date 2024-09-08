from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.components import Script

import numpy as np
from collections import namedtuple
from math import log10

NumberLine = namedtuple("NumberLine",["name","line"])
Tick = namedtuple("Tick",["x","size", "label"])

tick_style = {
    "big": {"length": 4, "size": .3, "color": "black", "label": True, "label_color": "red", "label_size": "2"},
    "medium": {"length": 2, "size": .2, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    "small": {"length": 1, "size": .1, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
}

hdrs = [Script(src="drag.js"),Script(src="https://raw.githubusercontent.com/Fflath/svg-ext/main/svg_ext.js"),Script(src="https://d3js.org/d3.v7.min.js")]

app, rt = fast_app(live=True, hdrs=hdrs)

start_x = 25
start_y = 5
width   = 100
arm_height = 10
slider_height = 10
scale = 10
buffer = 5

def mk_tick(y,tick,up,scale=1,start_x=start_x):
    d = 1 if up else -1
    return G(
        Line(x1=f"{start_x+tick.x*scale}", y1=f"{y}", x2=f"{start_x+tick.x*scale}", 
             y2=f"{y-tick_style[tick.size]['length']*d}", 
             stroke=tick_style[tick.size]['color'],
             stroke_width=tick_style[tick.size]['size']),

        Text(tick.label,x=f"{start_x+tick.x*scale}", y=f"{y-(.3+tick_style[tick.size]["length"])*d}", 
             fill=tick_style[tick.size]["label_color"], 
             font_size=tick_style[tick.size]["label_size"], text_anchor="middle", alignment_baseline="middle", 
             font_family="sans-serif", font_weight="bold") if tick_style[tick.size]["label"] else None
    )


line_options = {
    "integers-basic": "integers-basic",
    "log-basic": "log-basic",
    "reverse-log-basic": "reverse-log-basic",
    "split-pi-log-basic": "split-pi-log-basic"
}

def integer_line(x=start_x, y=start_y, width=width, up=True):
    bt = [Tick(x=tick,size="big",label=str(tick)) for tick in np.arange(0,10.1,1)]
    mt = [Tick(x=tick,size="medium", label=str(tick)) for tick in np.arange(0,10.1,.5)]
    st = [Tick(x=tick,size="small", label=str(tick)) for tick in np.arange(0,10.1,.1)]
    return mk_number_line(x,y,width,bt+mt+st,up)

def log_line(x=start_x, y=start_y, width=width, up=True):
    bt = [Tick(x=np.log10(tick)*10,size="big",label=str(tick)) for tick in np.arange(1,10.1,1)]
    mt = [Tick(x=np.log10(tick)*10,size="medium", label=str(tick)) for tick in np.arange(1,10.1,.5)]
    st = [Tick(x=np.log10(tick)*10,size="small", label=str(tick)) for tick in np.arange(1,10.1,.1)]
    return mk_number_line(x,y,width,bt+mt+st,up)

def reverse_log_line(x=start_x, y=start_y, width=width, up=True):
    bt = [Tick(x=10-np.log10(tick)*10,size="big",label=str(tick)) for tick in np.arange(1,10.1,1)]
    mt = [Tick(x=10-np.log10(tick)*10,size="medium", label=str(tick)) for tick in np.arange(1,10.1,.5)]
    st = [Tick(x=10-np.log10(tick)*10,size="small", label=str(tick)) for tick in np.arange(1,10.1,.1)]
    return mk_number_line(x,y,width,bt+mt+st,up)

def split_pi_log_line(x=start_x, y=start_y, width=width, up=True):
    bt = [Tick(x=np.log10(tick)*10,size="big",label=str(tick)) for tick in np.arange(1,10.1,1)]
    mt = [Tick(x=np.log10(tick)*10,size="medium", label=str(tick)) for tick in np.arange(1,10.1,.5)]
    st = [Tick(x=np.log10(tick)*10,size="small", label=str(tick)) for tick in np.arange(1,10.1,.1)]

    ltp = [Tick(x=(3.14-tick.x),size=tick.size, label=tick.label) for tick in (bt+mt+st) if tick.x < 3.14]
    gtp = [Tick(x=(10+3.14-tick.x),size=tick.size, label=tick.label) for tick in bt+mt+st if tick.x > 3.14]

    return mk_number_line(x,y,width,ltp+gtp,up)


def mk_number_line(x, y, width, ticks, up):
    return G(
        Line(x1=f"{x}", y1=f"{y}", x2=f"{x+width}", y2=f"{y}", stroke="black", stroke_width=".2"),
        *[mk_tick(y,tick,up,10,x) for tick in ticks]
    )

def mk_arms(x=start_x, y=start_y, width=width, arm_height=arm_height, slider_height=slider_height):
    return G(
        Rect(x=f"{x-buffer}", y=f"{y}", width=f"{width+2*buffer}", height=f"{arm_height}", fill="pearl", id="arm-top"),
        Rect(x=f"{x-buffer}", y=f"{y+arm_height+slider_height}", width=f"{width+2*buffer}", height=f"{arm_height}", fill="pearl", id="arm-bottom"),
        Rect(x=f"{x-buffer}", y=f"{y}", width=f"{buffer-2}", height=f"{slider_height+2*arm_height}", fill="#B77729", id="end-left"),
        Rect(x=f"{x+width+2}", y=f"{y}", width=f"{buffer-2}", height=f"{slider_height+2*arm_height}", fill="#B77729", id="end-right"),
        G(id="top-arm-lines",hx_ext="svg-ext"),
        G(id="bottom-arm-lines",hx_ext="svg-ext"),
        id="arms",
    )

def mk_slider(x=start_x, y=start_y, width=width, arm_height=arm_height, slider_height=slider_height):
    return G(
        Rect(
        x=f"{x-buffer}", 
        y=f"{y+arm_height}", 
        width=f"{width+2*buffer}", 
        height=f"{slider_height}", 
        fill="#007bff", 
        id="slider",
        stroke="black",
        stroke_width=".1",
    ),
    G(id="slider-lines-top",hx_ext="svg-ext"),
    G(id="slider-lines-bottom",hx_ext="svg-ext"),
    id="slider-group")

def mk_indicator(x=start_x, y=start_y, width=width, arm_height=arm_height, slider_height=slider_height):
    return G(
        Line(x1=f"{x + width/2+10}", y1=f"{y - 2}", x2=f"{x + width/2+10}", y2=f"{y + 2*arm_height+slider_height+4}", stroke="black", stroke_width=".1"),
        Rect(
        x=f"{x + width/2}",  # Center the indicator on the slider
        y=f"{y - 2}",
        width=f"{20}",
        height=f"{2*arm_height+slider_height+4}",
        fill="rgba(200, 100, 100, 0.5)",  # Semi-transparent red
    ),id="indicator")

def mk_ruler(x=start_x, y=start_y, width=width, arm_height=arm_height, slider_height=slider_height):
    return G(
        mk_slider(x, y, width, arm_height, slider_height),
        mk_arms(x, y, width, arm_height, slider_height),
        mk_indicator(x, y, width, arm_height, slider_height),
        id="ruler"
    )

@rt("/change/{target}/{attribute}/{value}")
def change(target: str, attribute: str, value: str):
    return Rect(**{"id": target,attribute:value})

init_x = 5

@app.get('/')
def homepage():
    return Div(
        NotStr('''<script>
                add_drag('#indicator');
                add_drag('#slider-group');
                add_drag('#arms');
               </script>'''),
        Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 150 50", id="svg-box")(
            mk_ruler(),
        ),
        Group(
            mk_function_dropdowns(function_options),
            mk_placement_dropdowns("Top Arm", "top-arm-lines", line_options),
            mk_placement_dropdowns("Top Slider", "slider-lines-top", line_options),
            mk_placement_dropdowns("Bottom Slider", "slider-lines-bottom", line_options),
            mk_placement_dropdowns("Lower Arm", "bottom-arm-lines", line_options)
        ),
    )


function_options= ["addition", "multiplication", "inverse"]

def mk_function_dropdowns(options):
    return Form(Select(name="value", hx_get=f"/function")(
        Option(f'-- Function --', disabled='', selected='', value=''),
        *[Option(item,value=item) for item in options], 
    ))

def mk_placement_dropdowns(p_name, p_val, options):
    return Form(Select(name="value", hx_get=f"/set/{p_val}", hx_swap="innerSVG", hx_ext="svg-ext", hx_target=f"#{p_val}")(
        Option(f'-- {p_name} --', disabled='', selected='', value=''),
        *[Option(name,value=val) for name,val in options.items()], 
    ))

placement_map = {
    "Upper Arm": "top-arm-lines",
    "Top of Slider": "slider-lines-top",
    "Bottom of Slider": "slider-lines-bottom",
    "Lower Arm": "bottom-arm-lines"
}

setting_map = {
    "top-arm-lines": {"y": start_y+arm_height - .1,"up": True},
    "slider-lines-top": {"y": start_y + arm_height + .1,"up": False},
    "slider-lines-bottom": {"y": start_y + arm_height + slider_height - .1,"up": True},
    "bottom-arm-lines": {"y": start_y + arm_height + slider_height + .1,"up": False}
}

@rt("/set/{position}")
def get(position: str, value: str):
    match value:
        case "integers-basic":
            return integer_line(**setting_map[position])
        case "log-basic":
            return log_line(**setting_map[position])
        case "reverse-log-basic":
            return reverse_log_line(**setting_map[position])
        case "split-pi-log-basic":
            return split_pi_log_line(**setting_map[position])

@rt("/function")
def get_function(value: str):
    match value:
        case "addition":
            return Div(
                    integer_line(**setting_map["top-arm-lines"])(hx_target="#top-arm-lines",hx_swap="innerSVG",hx_swap_oob="innerSVG:#top-arm-lines",hx_ext="svg-ext"),
                    integer_line(**setting_map["slider-lines-top"])(hx_target="#slider-lines-top",hx_swap="innerSVG",hx_swap_oob="innerSVG:#slider-lines-top",hx_ext="svg-ext"),
            )
        case "multiplication":
            return Div(
                log_line(**setting_map["top-arm-lines"])(hx_target="#top-arm-lines",hx_swap="innerSVG",hx_swap_oob="innerSVG:#top-arm-lines",hx_ext="svg-ext"),
                log_line(**setting_map["slider-lines-top"])(hx_target="#slider-lines-top",hx_swap="innerSVG",hx_swap_oob="innerSVG:#slider-lines-top",hx_ext="svg-ext"),
                )
        case "inverse":
            return Div(
                log_line(**setting_map["top-arm-lines"])(hx_target="#top-arm-lines",hx_swap="innerSVG",hx_swap_oob="innerSVG:#top-arm-lines",hx_ext="svg-ext"),
                reverse_log_line(**setting_map["slider-lines-top"])(hx_target="#slider-lines-top",hx_swap="innerSVG",hx_swap_oob="innerSVG:#slider-lines-top",hx_ext="svg-ext"),
                )

serve()
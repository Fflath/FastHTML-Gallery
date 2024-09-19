from fasthtml.common import *
from fasthtml.svg import *
from lines import *

# Constants
START_X = 10
START_Y = 5
WIDTH = 125
ARM_HEIGHT = 12
SLIDER_HEIGHT = 16.5
BUFFER = 5

tick_style = {
    "big": {"length": 2, "size": .3, "color": "black", "label": True, "label_color": "red", "label_size": "1"},
    "medium": {"length": 2, "size": .1, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    "small": {"length": 1, "size": .1, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    "tiny": {"length": .5, "size": .05, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    "none": {"length": 0, "size": 0, "color": "black", "label": False, "label_color": "black", "label_size": "0"},
}

setting_map = {
    "top-arm-3": {"y": START_Y+ARM_HEIGHT - .1,"up": True},
    "top-arm-2": {"y": START_Y+ARM_HEIGHT - 4.1,"up": True},
    "top-arm-1": {"y": START_Y+ARM_HEIGHT - 8.1,"up": True},
    "slider-1": {"y": START_Y + ARM_HEIGHT + .1,"up": False},
    "slider-2": {"y": START_Y + ARM_HEIGHT + 3.6,"up": False},
    "slider-3": {"y": START_Y + ARM_HEIGHT + 9.7,"up": True},
    "slider-4": {"y": START_Y + ARM_HEIGHT + 13,"up": True},
    "slider-5": {"y": START_Y + ARM_HEIGHT + SLIDER_HEIGHT - .1,"up": True},
    "bottom-arm-1": {"y": START_Y + ARM_HEIGHT + SLIDER_HEIGHT + .1,"up": False},
    "bottom-arm-2": {"y": START_Y + ARM_HEIGHT + SLIDER_HEIGHT + 3.1,"up": False},
    "bottom-arm-3": {"y": START_Y + ARM_HEIGHT + SLIDER_HEIGHT + 6.1,"up": False}
}

placement_map = {
    "Upper 1": "top-arm-1",
    "Upper 2": "top-arm-2",
    "Upper 3": "top-arm-3",
    "Slider 1": "slider-1",
    "Slider 2": "slider-2",
    "Slider 3": "slider-3",
    "Slider 4": "slider-4",
    "Lower 1": "bottom-arm-1",
    "Lower 2": "bottom-arm-2",
    "Lower 3": "bottom-arm-3"
}

def mk_number_line(line, placement, x=10, width=WIDTH, up=True):
    y = setting_map[placement]["y"]
    up = setting_map[placement]["up"]
    d = 1 if up else -1

    return [
        SvgOob(
            G(Line(x1=f"{x}", y1=f"{y}", x2=f"{x+width}", y2=f"{y}", stroke="black", stroke_width=".2"),
            *[mk_tick(y,tick,up,x) for tick in line.ticks]), hx_swap_oob=f"innerHTML:#{placement}"),
        SvgOob(
            Text(line.name, x=f"{x - 3.5}", y=f"{y-2.5*d}", fill="black", font_size="1", text_anchor="middle", alignment_baseline="middle", font_family="sans-serif", font_weight="bold"),
            hx_swap_oob=f"innerHTML:#label-{placement}-l"),
        SvgOob(
            Text(line.name, x=f"{x+width+3.5}", y=f"{y-2.5*d}", fill="black", font_size="1", text_anchor="middle", alignment_baseline="middle", font_family="sans-serif", font_weight="normal"),
            hx_swap_oob=f"innerHTML:#label-{placement}-r")]

def mk_tick(y,tick,up,start_x=5):
    d = 1 if up else -1
    return G(
        Line(x1=f"{start_x+tick.position}", y1=f"{y}", x2=f"{start_x+tick.position}", 
             y2=f"{y-tick_style[tick.style]['length']*d}", 
             stroke=tick_style[tick.style]['color'],
             stroke_width=tick_style[tick.style]['size']),
        Text(f"{tick.label:.0f}",x=f"{start_x+tick.position}", y=f"{y-(.5+tick_style[tick.style]["length"])*d}", 
             fill=tick_style[tick.style]["label_color"], 
             font_size=tick_style[tick.style]["label_size"], text_anchor="middle", alignment_baseline="middle", 
             font_family="sans-serif", font_weight="bold") if tick_style[tick.style]["label"] else None
    )

def mk_arms(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT, buffer=BUFFER):
    return G(
        Rect(x=f"{x-buffer}", y=f"{y}", width=f"{width+2*buffer}", height=f"{arm_height}", fill="pearl", id="arm-top"),
        Rect(x=f"{x-buffer}", y=f"{y+arm_height+slider_height}", width=f"{width+2*buffer}", height=f"{arm_height}", fill="pearl", id="arm-bottom"),
        Rect(x=f"{x-buffer}", y=f"{y}", width=f"{buffer-2}", height=f"{slider_height+2*arm_height}", fill="#B77729", id="end-left"),
        Rect(x=f"{x+width+2}", y=f"{y}", width=f"{buffer-2}", height=f"{slider_height+2*arm_height}", fill="#B77729", id="end-right"),
        G(id="top-arm-1"),
        G(id="top-arm-2"),
        G(id="top-arm-3"),
        G(id="bottom-arm-1"),
        G(id="bottom-arm-2"),
        G(id="bottom-arm-3"),

        G(id="label-top-arm-1-l"),
        G(id="label-top-arm-1-r"),
        G(id="label-top-arm-2-l"),
        G(id="label-top-arm-2-r"),
        G(id="label-top-arm-3-l"),
        G(id="label-top-arm-3-r"),

        G(id="label-bottom-arm-1-l"),
        G(id="label-bottom-arm-1-r"),
        G(id="label-bottom-arm-2-l"),
        G(id="label-bottom-arm-2-r"),
        G(id="label-bottom-arm-3-l"),
        G(id="label-bottom-arm-3-r"),

        G(id="label-slider-1-l"),
        G(id="label-slider-1-r"),
        G(id="label-slider-2-l"),
        G(id="label-slider-2-r"),
        G(id="label-slider-3-l"),
        G(id="label-slider-3-r"),
        G(id="label-slider-4-l"),
        G(id="label-slider-4-r"),
        G(id="label-slider-5-l"),
        G(id="label-slider-5-r"),
        id="arms",
    )

def mk_slider(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT, buffer=BUFFER):
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
    G(id="slider-1"),
    G(id="slider-2"),
    G(id="slider-3"),
    G(id="slider-4"),
    G(id="slider-5"),
    id="slider-group")

def mk_indicator(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT):
    return G(
        Line(x1=f"{x + width/2+10}", y1=f"{y - 2}", x2=f"{x + width/2+10}", y2=f"{y + 2*arm_height+slider_height+2}", stroke="black", stroke_width=".1"),
        Rect(
        x=f"{x + width/2}",  # Center the indicator on the slider
        y=f"{y - 2}",
        width=f"{20}",
        height=f"{2*arm_height+slider_height+4}",
        fill="rgba(200, 100, 100, 0.5)",  # Semi-transparent red
    ),id="indicator")

def mk_ruler(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT, buffer=BUFFER):
    return G(
        mk_slider(x, y, width, arm_height, slider_height, buffer),
        mk_arms(x, y, width, arm_height, slider_height, buffer),
        mk_indicator(x, y, width, arm_height, slider_height),
        id="ruler"
    )


def mk_function_dropdowns(options):
    return Form(Select(name="value", hx_get=f"/function")(
        Option(f'-- Function --', disabled='', selected='', value=''),
        *[Option(item,value=item) for item in options], 
    ))

def mk_placement_dropdowns(p_name, p_val, options):
    return Form(
        Select(name="value", hx_get=f"/set/{p_val}", hx_swap="innerSVG", hx_ext="svg-ext", hx_target=f"#{p_val}")(
        Option(f'-- {p_name} --', disabled='', selected='', value=''),
        *[Option(name,value=val) for name,val in options.items()], 
    ))

def mk_scale_swap(ruler_name):

    # return SvgOob(mk_number_line(C,**setting_map["slider-4"]),hx_swap_oob="innerHTML:#slider-4"),SvgOob(mk_number_line(C,**setting_map["slider-1"]),hx_swap_oob="innerHTML:#slider-1")
    r = ruler_options.get(ruler_name,None)
    # scales = [mk_number_line(scale["scale"], scale["position"]) for scale in r["scales"]]
    return [mk_number_line(scale["scale"], scale["position"]) for scale in r["scales"]]
from fasthtml.common import *
from fasthtml.svg import *
from lines import *
from constants import *
import json
# Constants

tick_style = {
    REAL_BIG: {"length": 2, "size": .3, "color": "black", "label": True, "label_color": "black", "label_size": "1.2"},
    BIG_MEDIUM: {"length": 2, "size": .3, "color": "black", "label": True, "label_color": "black", "label_size": "1"},
    BIG: {"length": 2, "size": .3, "color": "black", "label": True, "label_color": "black", "label_size": "1"},
    MEDIUM: {"length": 2, "size": .1, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    SMALL: {"length": 1, "size": .1, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    TINY: {"length": .5, "size": .05, "color": "black", "label": False, "label_color": "black", "label_size": "1"},
    NONE: {"length": .5, "size": .05, "color": "black", "label": False, "label_color": "black", "label_size": "1"},

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


def mk_number_line(line, placement, x=10, width=WIDTH, up=True, zoom=False):
    y = setting_map[placement]["y"] + (0 if not zoom else 45)
    up = setting_map[placement]["up"]
    zoomlabel = "zoom-" if zoom else ""
    d = 1 if up else -1
    return [
        SvgOob(
            G(Line(x1=f"{x}", y1=f"{y}", x2=f"{x+width}", y2=f"{y}", stroke="black", stroke_width=".2"),
            *[mk_tick(y,tick,up,x,zoom=zoom) for tick in line.ticks],id="lines",line=line.name), hx_swap_oob=f"innerHTML:#{zoomlabel}{placement}"),
        SvgOob(
            Text(line.name, x=f"{x - 3.5}", y=f"{y-2.5*d}", fill="black", font_size="1", text_anchor="middle", alignment_baseline="middle", font_family="sans-serif", font_weight="bold"),
            hx_swap_oob=f"innerHTML:#{zoomlabel}label-{placement}-l"),
        SvgOob(
            Text(line.name, x=f"{x+width+3.5}", y=f"{y-2.5*d}", fill="black", font_size="1", text_anchor="middle", alignment_baseline="middle", font_family="sans-serif", font_weight="normal"),
            hx_swap_oob=f"innerHTML:#{zoomlabel}label-{placement}-r")]

def mk_tick(y,tick,up,start_x=5,zoom=False):
    
    d = 1 if up else -1
    if not zoom:
        text_label = f"{tick.label:.0f}"
    elif round(tick.label,0) == round(tick.label,2): text_label = f"{tick.label:.0f}"    
    elif round(tick.label,1) == round(tick.label,2): text_label = f"{tick.label:.1f}"
    else: text_label = f"{tick.label:.2f}"
    return G(x=tick.x,id="tick")(
        Line(x1=f"{start_x+tick.position}", y1=f"{y}", x2=f"{start_x+tick.position}", 
             y2=f"{y-tick_style[tick.style]['length']*d}", 
             stroke=tick_style[tick.style]['color'],
             stroke_width=tick_style[tick.style]['size']),
        Text(text_label,x=f"{start_x+tick.position}", y=f"{y-(.5+tick_style[tick.style]["length"])*d}", 
             fill=tick_style[tick.style]["label_color"], 
             font_size=tick_style[tick.style]["label_size"], text_anchor="middle", alignment_baseline="middle", 
             font_family="sans-serif", font_weight="bold") if tick_style[tick.style]["label"] else None
    )

def mk_arms(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT, buffer=BUFFER,zoom=False):
    zoom = "zoom-" if zoom else ""
    return G(
        Rect(x=f"{x-buffer}", y=f"{y}", width=f"{width+2*buffer}", height=f"{arm_height}", fill="pearl", id="arm-top"),
        Rect(x=f"{x-buffer}", y=f"{y+arm_height+slider_height}", width=f"{width+2*buffer}", height=f"{arm_height}", fill="pearl", id="arm-bottom"),
        Rect(x=f"{x-buffer}", y=f"{y}", width=f"{buffer-2}", height=f"{slider_height+2*arm_height}", fill="#B77729", id="end-left"),
        Rect(x=f"{x+width+2}", y=f"{y}", width=f"{buffer-2}", height=f"{slider_height+2*arm_height}", fill="#B77729", id="end-right"),
        G(id=f"{zoom}top-arm-1"),
        G(id=f"{zoom}top-arm-2"),
        G(id=f"{zoom}top-arm-3"),
        G(id=f"{zoom}bottom-arm-1"),
        G(id=f"{zoom}bottom-arm-2"),
        G(id=f"{zoom}bottom-arm-3"),

        G(id=f"{zoom}label-top-arm-1-l"),
        G(id=f"{zoom}label-top-arm-1-r"),
        G(id=f"{zoom}label-top-arm-2-l"),
        G(id=f"{zoom}label-top-arm-2-r"),
        G(id=f"{zoom}label-top-arm-3-l"),
        G(id=f"{zoom}label-top-arm-3-r"),

        G(id=f"{zoom}label-bottom-arm-1-l"),
        G(id=f"{zoom}label-bottom-arm-1-r"),
        G(id=f"{zoom}label-bottom-arm-2-l"),
        G(id=f"{zoom}label-bottom-arm-2-r"),
        G(id=f"{zoom}label-bottom-arm-3-l"),
        G(id=f"{zoom}label-bottom-arm-3-r"),

        G(id=f"{zoom}label-slider-1-l"),
        G(id=f"{zoom}label-slider-1-r"),
        G(id=f"{zoom}label-slider-2-l"),
        G(id=f"{zoom}label-slider-2-r"),
        G(id=f"{zoom}label-slider-3-l"),
        G(id=f"{zoom}label-slider-3-r"),
        G(id=f"{zoom}label-slider-4-l"),
        G(id=f"{zoom}label-slider-4-r"),
        G(id=f"{zoom}label-slider-5-l"),
        G(id=f"{zoom}label-slider-5-r"),
        id=f"{zoom}arms",x=f"{x}",width =f"{width+2*buffer}"
    )

def mk_slider(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT, buffer=BUFFER,zoom=False):
    zoom = "zoom-" if zoom else ""
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
    G(id=f"{zoom}slider-1"),
    G(id=f"{zoom}slider-2"),
    G(id=f"{zoom}slider-3"),
    G(id=f"{zoom}slider-4"),
    G(id=f"{zoom}slider-5"),
    id=f"{zoom}slider-group",x=f"{x}",width=f"{width+2*buffer}")

def mk_indicator(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT,zoom=False):
    zoom = "zoom-" if zoom else ""
    return G(
        Line(x1=f"{x + width/2}", y1=f"{y - 2}", x2=f"{x + width/2}", y2=f"{y + 2*arm_height+slider_height+2}", stroke="black", stroke_width=".1"),
        Rect(
        x=f"{x + width/2-width/20}",  # Center the indicator on the slider
        y=f"{y - 2}",
        width=f"{width/10}",
        height=f"{2*arm_height+slider_height+4}",
        fill="rgba(200, 100, 100, 0.5)"),id=f"{zoom}indicator",x=f"{x + width/2-width/20}",width=f"{width/10}")

def mk_skeleton(x=START_X, y=START_Y, width=WIDTH, arm_height=ARM_HEIGHT, slider_height=SLIDER_HEIGHT, buffer=BUFFER,zoom=False):
    return G(
        mk_slider(x, y, width, arm_height, slider_height, buffer,zoom),
        mk_arms(x, y, width, arm_height, slider_height, buffer,zoom),
        mk_indicator(x, y, width, arm_height, slider_height,zoom),
        id="ruler"
    )

class Ruler:
    def __init__(self,config):
        self.name = config["name"]
        self.description = config["description"]
        self.scales = config["scales"]

    def mk_ruler(self): 
        return [mk_number_line(scale["scale"](),scale['position'],zoom=False) for scale in self.scales]

    def mk_zoom(self, zoom_limits): 
        zl = json.loads(zoom_limits)
        return [mk_number_line(scale["scale"](float(zl[scale["name"]][0]),float(zl[scale["name"]][1]),zoom=True),scale['position'],zoom=True) for scale in self.scales]
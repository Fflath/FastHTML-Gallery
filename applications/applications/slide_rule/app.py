from fasthtml.common import *
from fasthtml.svg import *

from random import randrange

hdrs = [Script(src="svg_ext.js"),]

app, rt = fast_app(live=True, hdrs=hdrs)

from fasthtml.components import Script

def mk_arms(x=5,y=5,width=80,height=10,space=5):
    return G(
        Rect(x=f"{x}", y=f"{y}", width=f"{width}", height=f"{height}", fill="pearl", id="arm-top"),
        Rect(x=f"{x}", y=f"{y+height+space}", width=f"{width}", height=f"{height}", fill="pearl", id="arm-bottom"),
        id="arms",
    )


def mk_slider(x=5, y=20, width=10, height=10):
    # Add draggable functionality to the slider
    return Rect(
        x=f"{x}", 
        y=f"{y}", 
        width=f"{width}", 
        height=f"{height}", 
        fill="#007bff", 
        id="slider",
        stroke="black",
        stroke_width=".1",
        onmousedown="startDrag(evt)",
        onmousemove="drag(evt)",
        onmouseup="endDrag(evt)",
        onmouseleave="endDrag(evt)"
    )


def mk_ruler(x=5, y=15, width=80, height=5):
    return mk_arms(), mk_slider(x, y, width, height)

@rt("/change/{target}/{attribute}/{value}")
def change(target: str, attribute: str, value: str):
    return Rect(**{"id": target,attribute:value})

init_x = 5

@app.get('/')
def homepage():
    return Div(Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 100 50",id="svg-box")(mk_ruler()))
serve()
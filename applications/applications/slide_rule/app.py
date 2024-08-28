from fasthtml.common import *
from fasthtml.svg import *

from random import randrange

hdrs = [Script(src="svg_ext.js"),]

app, rt = fast_app(live=True, hdrs=hdrs)

from fasthtml.components import Script

def mk_arms(x=5,y=5,width=80,height=10,space=5):
    return Rect(x=f"{x}", y=f"{y}", width=f"{width}", height=f"{height}", fill="pearl", id="arm-top"), Rect(x=f"{x}", y=f"{y+height+space}", width=f"{width}", height=f"{height}", fill="pearl", id="arm-bottom")

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

def mk_button(id, target, attribute, attribute_value, change_function):
    return Button(id=id, hx_target=f"#{target}", 
                     hx_get=f"/change/{target}/{attribute}/{change_function(attribute_value)}",
                     hx_swap="svg-box:update",hx_ext="svg-ext")

def mk_left(x_val, dx=lambda x: x-1): return mk_button("left", "slider", "x", x_val, dx)
def mk_right(x_val, dx=lambda x: x+1): return mk_button("right", "slider", "x", x_val, dx)

@rt("/change/{target}/{attribute}/{value}")
def change(target: str, attribute: str, value: str):
    return Rect(**{"id": target,attribute:value}),mk_left(int(value))(hx_swap_oob="outerHTML:#left"),mk_right(int(value))(hx_swap_oob="outerHTML:#right")

init_x = 5

@app.get('/')
def homepage():

    return Div(Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 100 50",id="svg-box")(mk_ruler()), 
        mk_left(init_x), mk_right(init_x))

serve()
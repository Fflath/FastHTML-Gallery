from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.components import Script
import random

app, rt = fast_app(live=True, hdrs=[Script(src="svg_ext.js")])

be_count = 0

def innerSVG():
    return Circle(cx=10, cy=10, r=random.randint(1,10), fill="red")

def beforeEnd():
    global be_count
    be_count += 1
    return Rect(x=10, y=20+10*be_count, width=10, height=10, fill="blue")

@app.get('/')
def homepage():
    global be_count
    be_count = 0
    return Div(
        Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 150 50", id="svg-box")(
            G(id="ex-innerSVG", hx_ext="svg-ext", hx_swap="innerSVG", hx_target="#ex-innerSVG", hx_get="/innerSVG",hx_trigger="click")(innerSVG()),
            G(id="ex-beforeEnd", hx_ext="svg-ext", hx_swap="beforeEnd", hx_target="#ex-beforeEnd", hx_get="/beforeEnd",hx_trigger="click")(beforeEnd()),
        )
    )

@rt("/innerSVG")
def get():
    return innerSVG()

@rt("/beforeEnd")
def get():
    return beforeEnd()

serve()
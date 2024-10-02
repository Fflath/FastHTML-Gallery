from fasthtml.common import *
from fasthtml.svg import *
from lines import *
from ui import *
import json

hdrs = [Script(src="drag.js"),Script(src="https://d3js.org/d3.v7.min.js"),]

app, rt = fast_app(live=True, hdrs=hdrs, ws_hdr=True)

@app.get('/')
def homepage():
    return Div(
        Script('''add_drag('#indicator');
                  add_drag('#slider-group');
                  add_drag('#arms');'''),
        Svg(viewBox="0 0 150 100",id="svg-box")(
            mk_skeleton(),
            mk_skeleton(y=50,zoom=True)(id="zoom")
        ),
        Button("Swap",hx_get="/show/default"),
        Div(id="mouse-position")("Move your mouse")

    )

default_ruler = Ruler(acuman_600)

@rt("/show/{ruler}")
def get(ruler: str):
    return default_ruler.mk_ruler()

@rt("/get-mouse-position/{line_json}")
def get_mouse_position(line_json:str):
    return default_ruler.mk_zoom(line_json)



serve()
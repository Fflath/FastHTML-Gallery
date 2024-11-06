from fasthtml.common import *
from fasthtml.svg import *
from lines import *
from ui2 import *
import json

hdrs = [Script(src="drag.js"),Script(src="https://d3js.org/d3.v7.min.js"),MarkdownJS()]

app, rt = fast_app(live=True, hdrs=hdrs, ws_hdr=True)

# with open("explanations.md") as f:
#     explanations = f.read()

@app.get('/')
def homepage():
    skelly = Skeleton(2,3,2)
    return Div(
        # Script('''add_drag('#indicator');
                #   add_drag('#slider-group');
                #   add_drag('#arms');
                #   add_just_drag('#zoom-indicator');'''),
        Div(id="explainer")(
            # Div(explanations,cls="marked"),
            Div(""),
        ),
        Svg(viewBox="0 0 150 100",id="svg-box")(
            skelly.mk()
            # mk_skeleton(),
            # mk_skeleton(y=50,zoom=True)(id="zoom")
        ),
        # Div(hx_get="/show/default",hx_trigger="load"),
        Div(id="mouse-position")
    )

# default_ruler = Ruler(acuman_600)

# @rt("/show/{ruler}")
# def get(ruler: str):
#     return Ruler(acuman_600).mk_ruler()

# @rt("/get-mouse-position/{line_json}")
# def get_mouse_position(line_json:str):
#     return Ruler(acuman_600).mk_zoom(line_json)

serve()
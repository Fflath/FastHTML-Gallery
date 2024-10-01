from fasthtml.common import *
from fasthtml.svg import *
from lines import *
from ui import *

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
            mk_skeleton(y=50)(id="zoom")
        ),
        Button("Swap",hx_get="/show/default"),
        Div(id="mouse-position")("Move your mouse")

    )

@rt("/show/{ruler}")
def get(ruler: str):
    return mk_ruler(ruler)

@rt("/get-mouse-position/{ind_x}/{arm_x}/{slider_x}")
def get_mouse_position(ind_x:float, arm_x:float, slider_x:float):
    return Div(P(f"Indicator position: X: {ind_x}"),
               P(f"Arm position: X: {arm_x}"),
               P(f"Slider position: X: {slider_x}"), id="mouse-position")



serve()
from fasthtml.common import *
from fasthtml.svg import *
from lines import *
from ui import *

hdrs = [Script(src="drag.js"),Script(src="https://d3js.org/d3.v7.min.js"),]

app, rt = fast_app(live=True, hdrs=hdrs)

@app.get('/')
def homepage():
    return Div(
        Script('''add_drag('#indicator');
                  add_drag('#slider-group');
                  add_drag('#arms');'''),
        Svg(viewBox="0 0 150 50",id="svg-box")(
            mk_skeleton()
        ),
        Button("Swap",hx_get="/show/default")
    )

@rt("/show/{ruler}")
def get(ruler: str):
    return mk_ruler(ruler)


serve()
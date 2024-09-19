from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.components import Script

from typing import Callable

from lines import *
from ui import *

hdrs = [Script(src="drag.js"),Script(src="https://d3js.org/d3.v7.min.js")]

app, rt = fast_app(live=True, hdrs=hdrs)

@app.get('/')
def homepage():
    return Div(
        NotStr('''<script>
                add_drag('#indicator');
                add_drag('#slider-group');
                add_drag('#arms');
               </script>'''),
        Svg(viewBox="0 0 150 50",id="svg-box")(
            mk_ruler(),
        ),
        Button("Swap",hx_get="/show/default")
    )

@rt("/show/{ruler}")
def get(ruler: str):
    return mk_scale_swap(ruler)


serve()
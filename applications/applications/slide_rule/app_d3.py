from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.components import Script


hdrs = [Script(src="svg_ext.js"),Script(src="https://d3js.org/d3.v7.min.js")]

app, rt = fast_app(live=True, hdrs=hdrs)

start_x = 25
start_y = 5
width   = 100
arm_height = 10
slider_height = 10


def integer_line(x, y, width, up):
    bt = [x for x in range(0,100,10)]
    mt = [x for x in range(0,100,5) if x not in bt]
    st = [x for x in range(0,100,1) if x not in bt and x not in mt]
    return mk_number_line(x,y,width,bt,mt,st,up)


def mk_number_line(x, y, width, big_ticks, medium_ticks, small_ticks,up):
    d = 1 if up else -1
    return G(
        Line(x1=f"{x}", y1=f"{y}", x2=f"{x+width}", y2=f"{y}", stroke="black", stroke_width=".2"),
        *[Line(x1=f"{x+tick}",y1=f"{y-4*d}",x2=f"{x+tick}",y2=f"{y}",stroke="black",stroke_width=".3") for tick in big_ticks],
        *[Line(x1=f"{x+tick}",y1=f"{y-2*d}",x2=f"{x+tick}",y2=f"{y}",stroke="black",stroke_width=".2") for tick in medium_ticks],
        *[Line(x1=f"{x+tick}",y1=f"{y-1*d}",x2=f"{x+tick}",y2=f"{y}",stroke="black",stroke_width=".1") for tick in small_ticks]
    )

def mk_arms(x, y, width, arm_height, slider_height):
    return G(
        Rect(x=f"{x}", y=f"{y}", width=f"{width}", height=f"{arm_height}", fill="pearl", id="arm-top"),
        Rect(x=f"{x}", y=f"{y+arm_height+slider_height}", width=f"{width}", height=f"{arm_height}", fill="pearl", id="arm-bottom"),
        id="arms",
    )

def mk_slider(x, y, width, arm_height, slider_height):
    return G(Rect(
        x=f"{x}", 
        y=f"{y+arm_height}", 
        width=f"{width}", 
        height=f"{slider_height}", 
        fill="#007bff", 
        id="slider",
        stroke="black",
        stroke_width=".1",
    ), id="slider-group")

def mk_indicator(x, y, width, arm_height, slider_height):
    return G(
        Line(x1=f"{x + width/2+10}", y1=f"{y - 2}", x2=f"{x + width/2+10}", y2=f"{y + 2*arm_height+slider_height+4}", stroke="black", stroke_width=".1"),
        Rect(
        x=f"{x + width/2}",  # Center the indicator on the slider
        y=f"{y - 2}",
        width=f"{20}",
        height=f"{2*arm_height+slider_height+4}",
        fill="rgba(200, 100, 100, 0.5)",  # Semi-transparent red
    ),id="indicator")


def mk_ruler(x, y, width, arm_height, slider_height):
    return mk_arms(x, y, width, arm_height, slider_height), mk_slider(x, y, width, arm_height, slider_height),mk_indicator(x, y, width, arm_height, slider_height)

@rt("/change/{target}/{attribute}/{value}")
def change(target: str, attribute: str, value: str):
    return Rect(**{"id": target,attribute:value})

init_x = 5

@app.get('/')
def homepage():
    return Div(
        NotStr('''<script>
                add_drag('#indicator');
                add_drag('#slider-group');
                add_drag('#arms');
               </script>'''),
        Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 150 50", id="svg-box")(
            mk_ruler(start_x,start_y,width,arm_height,slider_height),
            integer_line(start_x,start_y+.5*arm_height,width,up=True)),
    )

serve()
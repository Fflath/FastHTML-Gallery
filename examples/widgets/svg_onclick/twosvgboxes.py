from fasthtml.common import *
from fasthtml.svg import *

# SVG Extension
svg_ext = """
function svgExt(){
    htmx.defineExtension('svg-ext', {
        handleSwap: function(swapStyle, target, fragment, settleInfo) { 
            newSVG = document.createElementNS("http://www.w3.org/2000/svg",fragment.firstElementChild.tagName.toLowerCase())
            
            // Copy all attributes from newElem to newSVG
            for (let attr of fragment.firstElementChild.attributes) {
                newSVG.setAttributeNS(null, attr.name, attr.value);
            }

            document.querySelector(`#${swapStyle}`).appendChild(newSVG);
            htmx.process(document.body)

            target.remove()

            return true}
    })};
svgExt();
"""

app, rt = fast_app(live=True, hdrs=[Script(svg_ext),])

def mk_rect(width=5):
    return Rect(x="5", y="5", width=f"{width}", height="5", fill="#007bff", id="rect-1",
                hx_get=f"/increase_attribute/rect/{width}",hx_trigger=f"click",hx_target=f"#rect-1", hx_swap="svg-box-1",hx_ext="svg-ext")

def mk_circ(r=5):
    return Circle(cx="15", cy="15", r=f"{r}", fill="#007bff", id="circ-1",
                hx_get=f"/increase_attribute/circle/{r}",hx_trigger=f"click",hx_target=f"#circ-1", hx_swap="svg-box-2",hx_ext="svg-ext")

@rt("/increase_attribute/{shape}/{att}")
def get(shape: str, att: int):
    if shape == "circle":
        return mk_circ(att+1)
    else:
        return mk_rect(att+1)

@app.get('/')
def homepage():
    return  Div(
                Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 30 20",id="svg-box-1")(mk_rect()),
                Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 30 20",id="svg-box-2")(mk_circ()))

serve()
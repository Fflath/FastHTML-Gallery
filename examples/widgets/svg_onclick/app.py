from fasthtml.common import *
from fasthtml.svg import *

# SVG Extension
svg_ext = """
function svgExt(){
    htmx.defineExtension('svg-ext', {
        transformResponse: function(text, xhr, elt) { 
            const parser = new DOMParser();    
            newElem = parser.parseFromString(text, "image/svg+xml");
            newSVG = document.createElementNS("http://www.w3.org/2000/svg",'svgElem')
            // Copy all attributes from newElem to newSVG
            for (let attr of newElem.documentElement.attributes) {
                newSVG.setAttributeNS(null, attr.name, attr.value);
            }
            document.querySelector("#svg-box").appendChild(newSVG);
            htmx.process(document.body)
            return "" },
    })
    };
svgExt();
"""

app, rt = fast_app(live=True, hdrs=[Script(svg_ext),])

def mk_rect(width=5):
    return Rect(x="5", y="5", width=f"{width}", height="5", fill="#007bff", id="rect-1",
                hx_get=f"/increase_width/{width}",hx_trigger=f"click",hx_target=f"#rect-1", hx_swap="outerHTML",hx_ext="svg-ext")
    
@rt("/increase_width/{cw}")
def get(cw: int): return mk_rect(cw+1)

@app.get('/')
def homepage():
    return Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 30 20",id="svg-box")(
            mk_rect())

serve()
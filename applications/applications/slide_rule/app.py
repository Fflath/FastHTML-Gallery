from fasthtml.common import *
from fasthtml.svg import *

from random import randrange


# SVG Extension
svg_ext = """
function svgExt(){
    htmx.defineExtension('svg-ext', {
        transformResponse: function(text, xhr, elt) { 
            const parser = new DOMParser();    
            newElem = parser.parseFromString(text, "image/svg+xml");
            newSVG = document.createElementNS("http://www.w3.org/2000/svg",'rect')

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

hdrs = [Script(svg_ext),]

app, rt = fast_app(live=True, hdrs=hdrs)

from fasthtml.components import Script


def mk_rect(width):
    return Rect(x="4", y="5", width=f"{width}", height="10", fill="#007bff", id="draggable-rect",
                hx_get="/test",hx_trigger="click",hx_target="#draggable-rect", hx_swap="outerHTML",hx_ext="svg-ext")
    
@rt("/test")
def get(): return mk_rect(randrange(5, 20))

@app.get('/')
def homepage():

    title = "Slide Rule"
    return Title(title), Main(H1(title),
                              Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 30 20",id="svg-box")(mk_rect(10)))

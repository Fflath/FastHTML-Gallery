from fasthtml.common import *
from fasthtml.svg import *


svg_ext = """
function svgExt(){
    htmx.defineExtension('svg-ext', {
        handleSwap: function(swapStyle, target, fragment, settleInfo) { 
            var [svg_box,swap] = swapStyle.split(":")
            console.log(swapStyle,target,fragment,settleInfo)
            switch(swap){
            case "replace":
                newSVG = document.createElementNS("http://www.w3.org/2000/svg",fragment.firstElementChild.tagName.toLowerCase())
                for (let attr of fragment.firstElementChild.attributes) {
                    newSVG.setAttributeNS(null, attr.name, attr.value);
                }
                document.querySelector(`#${svg_box}`).appendChild(newSVG);
                htmx.process(document.body)
                target.remove()
                break;
            case "update":
                for (let attr of fragment.firstElementChild.attributes) {
                    target.setAttributeNS(null, attr.name, attr.value);
                }
                htmx.process(document.body)
                break;
            }
            return true}})};
            
svgExt();
"""

app, rt = fast_app(live=True, hdrs=[Script(svg_ext),])

def rect(x, y, width, height, id): return mk_rect(x=f"{x}", y=f"{y}", width=f"{width}", height=f"{height}", fill="blue", id=f"{id}")
def mk_rect(**kwargs): return Rect(**kwargs)

def mk_button(id,val): return Button(id="button",hx_get=f"/increase/{id}/height/{val+1}",hx_trigger="click",hx_target=f"#{id}", hx_swap="svg-box-1:update",hx_ext="svg-ext")

@rt("/increase/{id}/{att}/{val}")
def get(id: str, att: str, val: int):
    b = mk_button(id,val)(hx_swap_oob=f"outerHTML:#button")
    print(b)

    return mk_rect(id=id, **{att:val}),b


@app.get('/')
def homepage():
    return  Div(mk_button("rect1",2),
        Svg(xmlns="http://www.w3.org/2000/svg", viewBox="0 0 30 20",id="svg-box-1")(
            rect(5,5,5,2,"rect1")))

serve()
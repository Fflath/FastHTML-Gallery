(function svgExt(){
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
            return true}})})()

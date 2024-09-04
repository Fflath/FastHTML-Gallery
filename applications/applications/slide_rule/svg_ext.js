(function svgExt(){

    var api

    htmx.defineExtension('svg-ext', {
        // onEvent : function(name, evt) {
        //     if (name === 'htmx:oobBeforeSwap') {
        //         console.log("OOB Before Swap");
        //         console.log(evt);
        //         this.handleSwap(evt.detail.swapStyle, evt.detail.target, evt.detail.fragment, evt.detail.settleInfo);
        //         console.log("OOB After Swap");
        //     }
        //     // console.log("Fired event: " + name, evt);
        // },

        handleSwap: function(swapStyle, target, fragment, settleInfo) { 
            function add_children(target, node) {
                for (let child of node.children) {
                    add_child(target, child);
                }
            }
            function convertNS(node) {
                let newNode = document.createElementNS("http://www.w3.org/2000/svg", node.tagName.toLowerCase());
                for (let attr of node.attributes) {
                    newNode.setAttributeNS(null, attr.name, attr.value);
                }
                add_children(newNode, node);
                return newNode;
            }
            
            function add_child(target, child) {
                let newSVG = document.createElementNS("http://www.w3.org/2000/svg", child.tagName.toLowerCase());
                for (let attr of child.attributes) {
                    newSVG.setAttributeNS(null, attr.name, attr.value);
                }
                target.appendChild(newSVG);
                
                // Copy text content if present
                if (child.childNodes.length > 0) {
                    for (let node of child.childNodes) {
                        if (node.nodeType === Node.TEXT_NODE) {
                            newSVG.appendChild(document.createTextNode(node.textContent));
                        } else if (node.nodeType === Node.ELEMENT_NODE) {
                            add_child(newSVG, node);
            }}}};
            // Check if fragment is not a DocumentFragment and wrap it if necessary
            if (!(fragment instanceof DocumentFragment)) {
                let tempFragment = document.createDocumentFragment();
                tempFragment.appendChild(fragment);
                fragment = tempFragment;
            }
            switch(swapStyle){
            case "innerSVG":
                (function(){
                    let newSVGContainer = document.createElementNS("http://www.w3.org/2000/svg", fragment.firstElementChild.tagName.toLowerCase());
                    // Add attributes of the fragment's first child to newSVGContainer
                    for (let attr of fragment.firstElementChild.attributes) {
                        newSVGContainer.setAttributeNS(null, attr.name, attr.value);
                    }
                    for (let child of fragment.children) {
                        add_child(newSVGContainer, child);
                    }
                    while (target.firstChild) {
                        target.removeChild(target.firstChild);
                    }
                    target.appendChild(newSVGContainer);
                    htmx.process(document.body)})();
                break;
            case "outerSVG":
                (function(){
                    let newSVG = document.createElementNS("http://www.w3.org/2000/svg",fragment.firstElementChild.tagName.toLowerCase())
                    for (let attr of fragment.firstElementChild.attributes) {
                        newSVG.setAttributeNS(null, attr.name, attr.value);
                    }
                    target=newSVG;
                    htmx.process(document.body)
                    target.remove()})();
                break;
            case "update":
                for (let attr of fragment.firstElementChild.attributes) {
                    target.setAttributeNS(null, attr.name, attr.value);
                }
                htmx.process(document.body)
                break;
            case "beforeend":
                (function(){
                // let newSVGContainer = document.createElementNS("http://www.w3.org/2000/svg", fragment.firstElementChild.tagName.toLowerCase());
                // for (let attr of fragment.firstElementChild.attributes) {
                //     newSVGContainer.setAttributeNS(null, attr.name, attr.value);
                // }

                for (let child of fragment.children) {
                    add_child(newSVGContainer, child);
                }
                
                target.appendChild(newSVGContainer);
                htmx.process(document.body)})();
                break;
            }
            // api.oobSwap(swapStyle,target,settleInfo)
            return true}})})();

// htmx.logAll();

function add_drag(target) {
    document.addEventListener('DOMContentLoaded', (event) => {
    const svg = d3.select('#svg-box');
    const group = svg.select(target);

    const drag = d3.drag()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded);

    group.call(drag);

    function dragStarted(event) {
        d3.select(this).attr('cursor', 'grabbing');
    }

    function dragged(event) {
        const currentTransform = d3.select(this).attr('transform') || 'translate(0,0)';
        const currentTranslate = currentTransform.match(/translate\(([-\d.]+),\s*([-\d.]+)\)/) || [0, 0];
        const newX = parseFloat(currentTranslate[1] || 0) + event.dx;
        
        d3.select(this).attr('transform', `translate(${newX},0)`);
    }

    function dragEnded(event) {
        d3.select(this).attr('cursor', 'grab');
    }
})};
        

function startDrag(evt) {
    evt.target.setAttribute('data-dragging', 'true');
    evt.target.setAttribute('data-x', evt.clientX);
};

function drag(evt) {
    var el = evt.target;
    if (el.getAttribute('data-dragging') !== 'true') return;
    var dx = evt.clientX - parseFloat(el.getAttribute('data-x'));
    var newX = parseFloat(el.getAttribute('x')) + dx;
    el.setAttribute('x', newX);
    el.setAttribute('data-x', evt.clientX);
};
    
function endDrag(evt) {
    evt.target.setAttribute('data-dragging', 'false');
};
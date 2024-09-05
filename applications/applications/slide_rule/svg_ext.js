(function svgExt(){
    htmx.defineExtension('svg-ext', {

        handleSwap: function(swapStyle, target, fragment, settleInfo) { 
            function add_children(target, node) {
                for (let child of node.children) {
                    add_child(target, child);
                }
            }
            function convertNS(fragment) {
                let newSVGContainer = document.createElementNS("http://www.w3.org/2000/svg", fragment.firstElementChild.tagName.toLowerCase());
                for (let attr of fragment.firstElementChild.attributes) {
                    newSVGContainer.setAttributeNS(null, attr.name, attr.value);
                }
                add_children(newSVGContainer, fragment.firstElementChild);
                return newSVGContainer;
            }
            
            // Check if fragment is not a DocumentFragment and wrap it if necessary
            if (!(fragment instanceof DocumentFragment)) {
                let tempFragment = document.createDocumentFragment();
                tempFragment.appendChild(fragment);
                fragment = tempFragment;
            }
            let newSVGContainer = convertNS(fragment);

            switch(swapStyle){
            case "innerSVG":
                (function(){
                    while (target.firstChild) {
                        target.removeChild(target.firstChild);
                    }
                    target.appendChild(newSVGContainer);})();
                break;
            case "outerSVG":
                (function(){
                    target.parentNode.replaceChild(newSVGContainer, target);
                    target.remove()})();
                break;
            case "update":
                for (let attr of fragment.firstElementChild.attributes) {
                    target.setAttributeNS(null, attr.name, attr.value);
                }
                break;
            case "beforebeginSVG":
                (function(){target.parentNode.insertBefore(newSVGContainer, target)})();
                break;
            case "afterbeginSVG":
                (function(){target.insertBefore(newSVGContainer, target.firstChild)})();
                break;
            case "beforeendSVG":
                (function(){target.appendChild(newSVGContainer)})();
                break;
            case "afterendSVG":
                (function(){target.parentNode.append(newSVGContainer)})();
                break;
            case "deleteSVG":
                (function(){target.remove()})();
                break;
            }
            htmx.process(document.body)
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
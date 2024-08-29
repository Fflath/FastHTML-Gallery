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
            return true}})})();


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
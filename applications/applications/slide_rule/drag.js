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
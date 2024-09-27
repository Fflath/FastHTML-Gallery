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
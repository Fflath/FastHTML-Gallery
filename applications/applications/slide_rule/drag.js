function add_drag(target) {
    document.addEventListener('DOMContentLoaded', (event) => {
    const svg = d3.select('#svg-box');
    const ruler = svg.select('#ruler')
    const ind = ruler.select('#indicator')
    const arm = ruler.select('#arms')
    const slider = ruler.select('#slider-group')
    const group = ruler.select(target);

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
        // Find the leftmost tick underneath the indicator for each line
        const [indP_l,indP_r] = group_position(ind);

        const lines = ruler.selectAll('#lines');
        ret = {}
        lines.each(function() {
            const line = d3.select(this);
            const lg = d3.select(line.node().parentNode.parentNode)
            const [gp_l,gp_r] = group_position(lg)
            const ticks = line.selectAll('#tick');
            let leftTick = null;
            let rightTick = null;
            done = false
            ticks.each(function() {
                if (done) { return true }
                const tick = d3.select(this);
                const tickPosition = tick_position(tick,gp_l)
                if (leftTick === null && tickPosition >= indP_l) {
                    leftTick = tick;
                }
                if (leftTick !== null && rightTick === null && tickPosition > indP_r) {
                    rightTick = tick;
                    ret[line.attr("line")] = [leftTick.attr("x"),rightTick.attr("x")]
                    done = true
                }
            });
        });
        htmx.ajax('GET', `/get-mouse-position/${JSON.stringify(ret)}`, '#mouse-position')
    }
})};


function group_position(target) {
    currentTransform = target.attr('transform') || 'translate(0,0)';
    currentTranslate = currentTransform.match(/translate\(([-\d.]+),\s*([-\d.]+)\)/) || [0, 0];
    left = parseFloat(target.attr("x")) + parseFloat(currentTranslate[1])
    right = left + parseFloat(target.attr("width"))
    return [left, right]   
}

function tick_position(tick,gp_l) {
    const tline = tick.select('line')
    const tickPosition = parseFloat(tline.attr('x1')) + gp_l - 10;
    return tickPosition
}
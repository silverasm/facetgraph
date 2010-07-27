Raphael.fn.edge = function (obj1, obj2, line, bg) {
    if (obj1.line && obj1.from && obj1.to) {
        line = obj1;
        obj1 = line.from;
        obj2 = line.to;
    }
    var bb1 = obj1.getBBox(),
        bb2 = obj2.getBBox(),
        p = [{x: bb1.x + bb1.width / 2, y: bb1.y - 1},
        {x: bb1.x + bb1.width / 2, y: bb1.y + bb1.height + 1},
        {x: bb1.x - 1, y: bb1.y + bb1.height / 2},
        {x: bb1.x + bb1.width + 1, y: bb1.y + bb1.height / 2},
        {x: bb2.x + bb2.width / 2, y: bb2.y - 1},
        {x: bb2.x + bb2.width / 2, y: bb2.y + bb2.height + 1},
        {x: bb2.x - 1, y: bb2.y + bb2.height / 2},
        {x: bb2.x + bb2.width + 1, y: bb2.y + bb2.height / 2}],
        d = {}, dis = [];
    for (var i = 0; i < 4; i++) {
        for (var j = 4; j < 8; j++) {
            var dx = Math.abs(p[i].x - p[j].x),
                dy = Math.abs(p[i].y - p[j].y);
            if ((i == j - 4) || (((i != 3 && j != 6) || p[i].x < p[j].x) && ((i != 2 && j != 7) || p[i].x > p[j].x) && ((i != 0 && j != 5) || p[i].y > p[j].y) && ((i != 1 && j != 4) || p[i].y < p[j].y))) {
                dis.push(dx + dy);
                d[dis[dis.length - 1]] = [i, j];
            }
        }
    }
    if (dis.length == 0) {
        var res = [0, 4];
    } else {
        res = d[Math.min.apply(Math, dis)];
    }
    var x1 = p[res[0]].x,
        y1 = p[res[0]].y,
        x4 = p[res[1]].x,
        y4 = p[res[1]].y;
    dx = Math.max(Math.abs(x1 - x4) / 2, 10);
    dy = Math.max(Math.abs(y1 - y4) / 2, 10);
    var x2 = [x1, x1, x1 - dx, x1 + dx][res[0]].toFixed(3),
        y2 = [y1 - dy, y1 + dy, y1, y1][res[0]].toFixed(3),
        x3 = [0, 0, 0, 0, x4, x4, x4 - dx, x4 + dx][res[1]].toFixed(3),
        y3 = [0, 0, 0, 0, y1 + dy, y1 - dy, y4, y4][res[1]].toFixed(3);
    var path = ["M", x1.toFixed(3), y1.toFixed(3), "C", x2, y2, x3, y3, x4.toFixed(3), y4.toFixed(3)].join(",");
    if (line && line.line) {
        line.bg && line.bg.attr({path: path});
        line.line.attr({path: path});
    } else {
        var color = typeof line == "string" ? line : "#000";
        return {
            bg: bg && bg.split && this.path(path).attr({stroke: bg.split("|")[0], fill: "none", "stroke-width": bg.split("|")[1] || 3}),
            line: this.path(path).attr({stroke: color, fill: "none"}),
            from: obj1,
            to: obj2
        };
    }
};

var start = function(){
	this.ox = this.attr("cx");
	this.oy = this.attr("cy");
	for(var i = 0; i < this.inner.length; i++){
		var element = this.inner[i];
		var isX = (element.type == "text") || (element.type == "rect");
		element.ox = isX ? element.attr("x") : element.attr("cx");
        element.oy = isX ? element.attr("y") : element.attr("cy");
	}
},
move=function(dx, dy){
	/* Move the containing object*/
	this.attr({cx:this.ox+dx, cy:this.oy+dy});
	
	/* Move the inner components, like the text */
	for(var i = 0; i < this.inner.length; i++){
		var element = this.inner[i];
		var isX = (element.type == "text") || (element.type == "rect");
		if (isX){
			element.attr("x", element.ox + dx);
			element.attr("y", element.oy + dy);
		}else{
			element.attr("cx", element.ox + dx);
			element.attr("cy", element.oy + dy);
		}
	}
	
	/*Move the edges*/
	for (var i = edges.length; i--;) {
        paper.edge(edges[i]);
    }
    paper.safari();

},
stop = function(){};

var edges = [];
var nodes = {};
var colors = [];
var edgeColor = "#000";

function drawGraph(graph /*JSON graph object*/) {
	paper.clear();
	edges = [];
	nodes = {};
	for(var i = 0; i < graph.nodes.length; i++){
		var node = graph.nodes[i];
		if(node.level+1 > colors.length){
			colors.push(Raphael.getColor()); // choose next in spectrum
		}
		var c = paper.circle(node.position.x, node.position.y, 30);
		c.attr({fill:colors[node.level], stroke:"#fff", cursor:"move"});
		c.drag(move, start, stop);
		nodes[node.id] = c;
		//$("#debug").html($("#debug").html() +", "+node.id);
		c.inner = [];
		for(var j = 0; j < node.components.length; j++){
			var component = node.components[j];
			if(component.type == "text"){
				var t = paper.text(c.attr("cx"), c.attr("cy"), component.name);
				if(component.url){
					t.url = component.url;
					t.attr({cursor:"pointer"});
					t.click(function(){
						$.getJSON(this.url, function(data){
							drawGraph(data);
						});
					});
				}
				c.inner.push(t);
			}	
		}
	}
	for(var k = 0; k < graph.edges.length; k++){
		var edge = graph.edges[k];
		edges.push(paper.edge(nodes[edge.from], nodes[edge.to], edgeColor, "#888"));
	}
}




	
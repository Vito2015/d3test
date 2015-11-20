/**
 * Created by devnode on 15-11-19.
 */
function on_confirm(parent) {
    draw(parent);
}

// parent: jQuery object
function draw(parent) {
    //var initWidth = 960;
    var initWidth = 20000;//影响横轴的显示范围

    var stations = []; // lazily loaded

    var formatDateTime = d3.time.format("%Y%m%d%H%M%S");
    var formatDate = d3.time.format("%Y%m%d");
    var formatTime = d3.time.format("%H:%M");

    var margin = {top: 20, right: 30, bottom: 20, left: 100},
        width = initWidth - margin.left - margin.right,
        height = 700 - margin.top - margin.bottom;          // 700影响运行图高度

    var beginTime = "20140702045000";           // read from csv
    var endTime = "20140703020000";

    // 鼠标移动到列车线产生的tooltip
    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("font-size", "8px")
        .style("visibility", "hidden")
        .text("a simple tooltip");

    var x = d3.time.scale()
        .domain([parseTimeForAxis(beginTime), parseTimeForAxis(endTime)])
        //.range([0, width]);
        .range([0, 40000]);//影响横轴的单位时间的宽度

    var y = d3.scale.linear()
        .range([0, height]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .ticks(480)//有多少个横轴点, 80:30min, 160:15min, 480:5min
        .tickFormat(formatTime);

    var line = d3.svg.line()
        .x(function(d) { return x(d.time); })
        .y(function(d) { return y(d.station.distance); });

    //var svg_parent = $(parent);
    var svg = d3.select(parent.get(0)).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("defs").append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("y", -margin.top)
        .attr("width", width)
        .attr("height", height + margin.top + margin.bottom);


    //d3.csv("data/line01_20140702.csv", type, function(error, trains) {
    d3.csv("static/data/LINE01_PLAN_201407020000.tcsv", type, function(error, trains) {
        y.domain(d3.extent(stations, function(d) {
            //console.log(stations);
            return d.distance; }));

        var station = svg.append("g")
            .attr("class", "station")
            .selectAll("g")
            .data(stations)
            .enter().append("g")
            .attr("transform", function(d) {
                //console.log(d);
                return "translate(0," + y(d.distance) + ")"; });

        // 绘制左侧纵轴, y轴
        station.append("text")
            .attr("x", -6)
            .attr("dy", ".35em")
            .text(function(d) {
                //console.log(d);
                return d.name; });

        // 绘制横向背景线
        station.append("line")
            .attr("x2", width);

        // 绘制顶部横轴, x轴
        svg.append("g")
            .attr("class", "x top axis")
            .call(xAxis.orient("top"));

        // 绘制底部横轴, y轴
        svg.append("g")
            .attr("class", "x bottom axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis.orient("bottom"));

        var train = svg.append("g")
            .attr("class", "train")
            .attr("clip-path", "url(#clip)")
            .selectAll("g")
            .data(trains.filter(function(d) { return /[NLB]/.test(d.type); }))
            .enter().append("g")
            .attr("class", function(d) { return d.type; });

        // 绘制列车线
        train.append("path")
            .attr("d", function(d) { return line(d.stops); })
            .on("mouseover", function(d){
                tooltip.text("车次号: " + d.trip);
                return tooltip.style("visibility", "visible");})
            .on("mousemove", function(){ return tooltip.style("top",
                (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
            .on("mouseout", function(){ return tooltip.style("visibility", "hidden");});
        /*.on("mouseover", function() {
         d3.select(this).enter().append("text")
         .text(function(d) {return d.trip;})
         });*/

        // 绘制小圆点
        train.selectAll("circle")
            .data(function(d) { return d.stops; })
            .enter().append("circle")
            .attr("transform", function(d) { return "translate(" + x(d.time) + "," + y(d.station.distance) + ")"; })
            .attr("r", 2)              // 点直径
            .on("mouseover", function(d){
                var format = d3.time.format("%H:%M:%S");
                tooltip.text(format(d.time));
                d3.select(this).attr("r", "3");                                                       //<circle cx="168" cy="179" r="59"
                //fill="white" stroke="black"
                //onmouseover="evt.target.setAttribute('r', '72');"
                //onmouseout="evt.target.setAttribute('r', '59');"/>
                return tooltip.style("visibility", "visible");
            })
            .on("mousemove", function(){ return tooltip.style("top",
                (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
            .on("mouseout", function(){
                d3.select(this).attr("r", "2");
                return tooltip.style("visibility", "hidden");});
    });

    function type(d, i) {
        // Extract the stations from the "stop|*" columns.
        if (!i) for (var k in d) {
            if (/^stop\|/.test(k)) {
                var p = k.split("|");
                stations.push({
                    key: k,
                    name: p[1],
                    id: p[2],
                    distance: +p[3],
                    zone: +p[4]
                });
            }
        }

        return {
            trip: d.trip,
            type: d.type,
            direction: d.direction,
            stops: stations
                .map(function(s) { return {station: s, time: parseTimeForData(d[s.key])}; })
                .filter(function(s) { return s.time != null; })
        };
    }

    function parseTimeForAxis(s) {
        var t = formatDateTime.parse(s);
        if (t != null && t.getHours() < 3) t.setDate(t.getDate() + 1);
        return t;
    }

    function parseTimeForData(s) {
        var t = formatDateTime.parse(s);
        return t;
    }
}
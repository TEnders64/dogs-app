$(document).ready(function(){
    getRates(0);
    
    $("a").click(function(e){
        e.preventDefault();
        getRates($(this).attr("data-id"));
    })
    
})

function getRates(days){
    $.get(
        '/rates/past/'+days+'/json',
        function(response){
            data = JSON.parse(response);
            buildTable(data);
            buildGraph(data);
        },
        'json'
    );
}

function buildTable(data){
    let rates = data.map(function(rateObj){return rateObj.fields;})
    $("#rate-table tbody").html("");
    for (let i = 0; i < rates.length; i++){
        let dateFormat = d3.timeFormat("%b %e, %Y, %I:%M%p")
        let htmlStr = ` <tr>
                            <td>${dateFormat(new Date(rates[i].date))}</td>
                            <td>${rates[i].rate}</td>
                        </tr>
                      `
        $("#rate-table tbody").append(htmlStr);
    }
}

function buildGraph(data){
    $('svg').html("");
    let oldestDate = new Date(data[0].fields.date),
        newestDate = new Date(data[data.length-1].fields.date);
    
    let rates = data.map(function(rateObj){return rateObj.fields;})
    let ratesVals = rates.map(function(rate){return rate.rate});
    let maxRate = Math.max(...ratesVals);
    let minRate = Math.min(...ratesVals);

    let svgArea = $('#svg-area');
    let margin = {
        top: 20,
        right: 20,
        bottom: 20,
        left: 20
    }
    let padding = {
        top: 20,
        right: svgArea.css('paddingRight').replace("px",""),
        bottom: 20,
        left: svgArea.css('paddingLeft').replace("px","")
    }

    let innerWidth = svgArea.css('width').replace("px","") - margin.left - margin.right;
    let innerHeight = svgArea.css('height').replace("px","") - margin.top - margin.bottom;

    let width = innerWidth - padding.left - padding.right;
    let height = innerHeight - padding.top - padding.bottom;

    let svg = d3.select("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.bottom + margin.top)
                .append("g")
                .attr("transform", "translate("+margin.left+","+margin.top+")");
    
    let xScale = d3.scaleTime()
            .domain([new Date(newestDate), new Date(oldestDate)])
            .range([0,width]);
    let yScale = d3.scaleLinear()
            .domain([minRate, maxRate])
            .range([height,0]);

    let xAxis = d3.axisBottom(xScale)
            .ticks(10);
    let yAxis = d3.axisLeft(yScale)
            .ticks(10);

    svg.append("g")
        .attr("transform","translate(0,"+height+")")
        .call(xAxis);

    svg.append("g")
        .call(yAxis);
    
    let line = d3.line()
            .x(function(d){ return xScale(new Date(d.date)); })
            .y(function(d){ return yScale(d.rate); })
            .curve(d3.curveMonotoneX);
    
    svg.append("path")
        .datum(rates)
        .attr("class", "line")
        .attr("d", line);
}
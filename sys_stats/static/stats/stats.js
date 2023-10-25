// noinspection JSUnresolvedReference

let socket = io(`ws://${window.location.host}`);

function plotMemoryChart(percentage, total, used) {
    let data = [
        {
            domain: {x: [0, 1], y: [0, 1]},
            value: percentage,
            number: {suffix: "%"},
            title: {text: "Memory Usage - " + used + " MB of " + total + " MB"},
            type: "indicator",
            mode: "gauge+number",
            gauge: {
                axis: {
                    range: [0, 100],
                    tickwidth: 0,
                    tickformat: "",
                    tickcolor: "transparent"
                },
                bar: {
                    color: "blue"
                },
                bgcolor: "#bfd4f4",
                borderwidth: 2,
                bordercolor: "white",
            }
        }
    ];
    let config = {displayModeBar: false};
    let layout = {
        width: 500,
        height: 400,
        margin: {t: 0, b: 0}
    };
    Plotly.newPlot('memory-usage-chart', data, layout, config);
}

function plotCPUChart(percentage) {
    let data = [
        {
            domain: {x: [0, 1], y: [0, 1]},
            value: percentage,
            number: {suffix: "%"},
            title: {text: "CPU Usage"},
            type: "indicator",
            mode: "gauge+number",
            gauge: {
                axis: {
                    range: [0, 100],
                    tickwidth: 0,
                    tickformat: "",
                    tickcolor: "transparent"
                },
                bar: {
                    color: "blue"
                },
                bgcolor: "#bfd4f4",
                borderwidth: 2,
                bordercolor: "white",
            }
        }
    ];
    let config = {displayModeBar: false};
    let layout = {
        width: 500,
        height: 400,
        margin: {t: 0, b: 0}
    };
    Plotly.newPlot('memory-usage-chart1', data, layout, config);
}

function plotCPUCoresChart(percentageArray) {
    let xLabels = Object.keys(percentageArray).map(label => (parseInt(label) + 1).toString());
    let yValues = Object.values(percentageArray);

    var data = [
        {
            x: xLabels,
            y: yValues,
            type: 'bar'
        }
    ];

    var layout = {
        yaxis: {
            range: [0, 100],
            title: 'CPU Cores Usage (%)'
        },
        xaxis: {
            categoryorder: 'category ascending',
            tickmode: 'linear',
            title: 'CPU Cores' // Set x-axis label
        },
        height: 350
    };
    let config = {displayModeBar: false};

    Plotly.newPlot('cpu-cores-chart', data, layout, config);
}


$(document).ready(function () {
    $(function () {
        $('[data-bs-toggle="tooltip"]').tooltip();
    });

    console.log('Loaded socketio script');
    socket.on('connect', () => {
        console.log('Connected to server!');
        // socket.emit('list_processes', {data: 'foo!', id: 123});
    });

    setInterval(function () {
        socket.emit('resource_usage', {search_keyword: ''});
    }, 1000);

    socket.on("resource-usage", data => {
        // console.log("prc: " + JSON.stringify(data))
        let memory = data.memory;
        let cpu = data.cpu_usage;

        plotMemoryChart(memory.percent, memory.total, memory.used);
        plotCPUChart(cpu.combined);
        plotCPUCoresChart(cpu.per_cpu)
    });
});

$(document).on('click', '.expandable-cell', function () {
    let $cell = $(this);
    let isExpanded = $cell.hasClass('expanded');
    if (isExpanded) {
        $cell.removeClass('expanded');
    } else {
        $cell.addClass('expanded');
    }
});

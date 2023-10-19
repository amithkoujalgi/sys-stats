// noinspection JSUnresolvedReference


let socket = io("ws://0.0.0.0:8070");

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
        width: 600,
        height: 500,
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
        width: 600,
        height: 500,
        margin: {t: 0, b: 0}
    };
    Plotly.newPlot('memory-usage-chart1', data, layout, config);
}

$(document).ready(function () {
    let url = window.location.href;

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
        let cpuBody = $('.cpu-list');
        let cpuRows = ""
        let count = 1;
        for (let cpuItem of cpu.per_cpu) {
            let row = `
                <tr>
                    <td style="font-family: monospace">${count}</td>
                    <td style="font-family: monospace">${cpuItem} %</td>
                </tr>
            `;
            cpuRows = cpuRows + row;
            count = count + 1;
        }

        let cpuTbl = `
            <thead>
            <tr>
                <th scope="col">Core</th>
                <th scope="col">Usage (%)</th>
            </tr>
            </thead>
            <tbody>
            ${cpuRows}
            </tbody>
        `;
        cpuBody.html(cpuTbl);

        plotMemoryChart(memory.percent, memory.total, memory.used);
        plotCPUChart(cpu.combined);
    });
});

$(document).on('click', '#send', function () {
    console.log('clicked...')
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

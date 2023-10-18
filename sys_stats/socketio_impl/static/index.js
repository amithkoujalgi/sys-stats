// noinspection JSUnresolvedReference


let socket = io("ws://0.0.0.0:8070");

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
        socket.emit('list_processes', {search_keyword: ''});
    }, 1000);

    socket.on("process-list", data => {
        // console.log("prc: " + JSON.stringify(data))
        let processList = data;
        let tableBody = $('.process-list');

        let rows = "";
        for (let process of processList) {
            let row = `
                <tr>
                    <td style="font-family: monospace">${process.pid}</td>
                    <td style="font-family: monospace">${process.name}</td>
                    <td style="font-family: monospace">${process.username}</td>
                    <td class="process-status-container" style="font-family: monospace">${process.status}</td>
                    <td style="font-family: monospace">${process.running_since}</td>
                    <td style="font-family: monospace">${process.parent}</td>
                    <td style="font-family: monospace" class="contained expandable-cell" 
                        style="font-family: monospace" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title=${process.cmdline}>${process.cmdline}</td>
                    <td style="font-family: monospace">${process.memory_usage}</td>
                    <td style="font-family: monospace">${process.cpu_usage}</td>
                    <td style="font-family: monospace">Kill</td>
                </tr>
            `;
            rows = rows + row;
        }
        let head = `
                <thead>
                    <tr>
                        <th scope="col">PID</th>
                        <th scope="col">Name</th>
                        <th scope="col">User</th>
                        <th scope="col">Status</th>
                        <th scope="col">Running Since</th>
                        <th scope="col">Parent</th>
                        <th scope="col">Command</th>
                        <th scope="col">Memory usage</th>
                        <th scope="col">CPU usage</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
        `;
        tableBody.html(head + "<tbody>" + rows + "</tbody>");
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

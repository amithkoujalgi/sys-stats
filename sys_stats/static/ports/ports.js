// noinspection JSUnresolvedReference

let socket = io(`ws://${window.location.host}`);

$(document).ready(function () {
    $(function () {
        $('[data-bs-toggle="tooltip"]').tooltip();
    });

    console.log('Loaded socketio script');
    socket.on('connect', () => {
        console.log('Connected to server!');
    });

    setInterval(function () {
        socket.emit('list_ports', {search_keyword: $("#port-search").val()});
    }, 1000);

    socket.on("port-list", data => {
        // console.log("prc: " + JSON.stringify(data))
        let portsList = data;
        let tableBody = $('.port-list');

        let rows = "";
        for (let process of portsList) {
            let row = `
                <tr>
                    <td style="font-family: monospace">${process.pid}</td>
                    <td style="font-family: monospace">${process.laddr.port}</td>
                    <td style="font-family: monospace">${process.laddr.ip}</td>
                    <td class="process-status-container" style="font-family: monospace">${process.process_owner}</td>
                    <td style="font-family: monospace">${process.process_name}</td>
                    <td style="font-family: monospace">${process.process_cmd}</td>
                </tr>
            `;
            rows = rows + row;
        }
        let head = `
                <thead>
                   <tr>
                        <th scope="col">PID</th>
                        <th scope="col">Bind Port</th>
                        <th scope="col">Bind Host</th>
                        <th scope="col">User</th>
                        <th scope="col">Process</th>
                        <th scope="col">Command</th>
                    </tr>
                </thead>
        `;
        tableBody.html(head + "<tbody>" + rows + "</tbody>");
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

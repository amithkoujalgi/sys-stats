// noinspection JSUnresolvedReference

let socket = io(`ws://${window.location.host}`);

$(document).ready(function () {
    $(function () {
        $('[data-bs-toggle="tooltip"]').tooltip();
    });

    console.log('Loaded socketio script');
    socket.on('connect', () => {
        console.log('Connected to server!');
        socket.emit('list_processes', {search_keyword: ''});
    });

    setInterval(function () {
        socket.emit('list_processes', {search_keyword: $('#proc-search').val()});
    }, 1000);

    socket.on("process-kill-status", data => {
        $('.toast-body').html(`Process ${data.pid} killed.`);
        $('#toast').toast('show');
    });

    socket.on("process-list", data => {
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
                    <td style="font-family: monospace" class="kill-prc prc-${process.pid}">
                        <a href="#" class="nav-link py-3 px-2" style="color: red;" title=""
                           data-bs-toggle="tooltip"
                           data-bs-placement="right" data-bs-original-title="Terminate process">
                            <i class="bi-sign-stop fs-1"></i>
                        </a>
                    </td>
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

$(document).on('click', '.kill-prc', function () {
    let pid = $(this).attr('class').replace('kill-prc', '').replace('prc-', '').trim();
    const result = window.confirm(`Are you sure you want to kill this process (PID: ${pid})?`);
    if (result) {
        socket.emit('kill_process', {process_id: pid});
    }
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

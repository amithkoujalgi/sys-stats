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
});
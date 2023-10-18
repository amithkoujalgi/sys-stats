let socket = io("ws://0.0.0.0:8070");

console.log('Loaded socketio script')
socket.on('connect', () => {
    console.log('Connected to server!');
});
$(document).on('click', '#send', function () {
    console.log('emitting message...')
    socket.emit('my-action', {data: 'foo!', id: 123});
});
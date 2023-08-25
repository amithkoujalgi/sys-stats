// noinspection JSUnresolvedReference

$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
})
$(document).ready(function () {
    $('.expandable-cell').click(function () {
        let $cell = $(this);
        let isExpanded = $cell.hasClass('expanded');
        if (isExpanded) {
            $cell.removeClass('expanded');
        } else {
            $cell.addClass('expanded');
        }
    });
});

$(document).on('click', '.kill-process', function () {
    if (confirm('Are you sure you want to terminate this process?')) {
        let pid = this.id.replace('pid-', '');
        let url = $(location).attr('protocol') + '//' + $(location).attr('host') + `/kill/${pid}`;
        $.ajax({
            url: url,
            type: 'GET',
            contentType: "application/json; charset=utf-8",
            success: function (res) {
                console.log("Res: " + res);
                location.reload();
            },
            error: function (jqXHR, tranStatus, errorThrown) {
                console.log("Error: ");
                console.log('Status: ' + jqXHR.status + ' ' + jqXHR.statusText + '. ' + 'Response: ' + jqXHR.responseText);
            }
        });
    }
});
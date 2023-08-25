// noinspection JSUnresolvedReference

$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
});

$(document).ready(function () {
    let url = window.location.href;
    let searchKeyIndex = url.indexOf('search=')
    if (searchKeyIndex > 0) {
        let searchKeyword = url.substring(searchKeyIndex + 7, url.length);
        $("#proc-search").val(searchKeyword);
    } else {
        $("#proc-search").val('');
    }
});

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

$(document).ready(function () {
    const $searchInput = $("#proc-search");
    const $searchButton = $("#proc-search-btn");

    function performSearch() {
        const searchText = $searchInput.val();
        let apiUrl = $(location).attr('protocol') + '//' + $(location).attr('host') + `/?search=${encodeURIComponent(searchText)}`;
        window.location = apiUrl;
    }

    $searchInput.keyup(function (event) {
        if (event.key === "Enter") {
            performSearch();
        }
    });

    $searchButton.click(function () {
        performSearch();
    });
});
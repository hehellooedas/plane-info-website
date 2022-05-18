(function () {
    $.ajax(
        {
            type: 'get',
            url: '/settlement',
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                alert(data);
            }

        }
    )
})();
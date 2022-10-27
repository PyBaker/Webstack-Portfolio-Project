$( document ).ready(function () {
    /********************************
     Get aspirant clicked on checkbox
     changes: get asp_no and candidate name from this instead
     ********************************/
    let candidate;
    $('input[type=radio]').change(function () {
        if ($(this).is(':checked')) {
            candidate = $(this).attr('data-name');
        }
    });

    /*********************************
     Get the post name from html page
     *********************************/
    let post_name = $("#post_name").text()

    /***********************************
     Get the voter's information: id_no and reg_no
     ***********************************/


    /*************************************
     Define behaviour of the submit button
     **************************************/
    $("#submit_button").click(function () {
        $.ajax({
            type: 'PUT',
            url: 'http://0.0.0.0:5001/api/v1/vote',
            data: JSON.stringify({
                'post_name': post_name,
                'asp_no': asp_no,
                'id_no': id_no,
                'reg_no': reg_no
            }),
            contentType: 'application/json',
            success: function (data) {
                alert(`${data.res}`);
                
            }
        });
    });
});
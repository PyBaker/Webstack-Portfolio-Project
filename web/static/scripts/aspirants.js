window.load = function () {
    $( document ).ready(function () {
    /***************
     remove candidates div
     ***************/
    /*$("#candidates").remove()*/
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5001/api/v1/aspirants/president",
        data: JSON.stringify({}),
        contentType: 'application/json',
        success: function (data) {
            /*$("#candidate_label_1").text(`${data[0].First_Name}`);*/
            $("#candidate_label_1").text('Testing');

            console.log(`${data[0].First_Name}`);
        }

    })
});
}
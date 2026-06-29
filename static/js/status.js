$(document).ready(function () {
    console.log('status ok - REGIX Studio');

    $.ajax({
        type: "POST",
        url: "/get-process",
        success: function (response) {
            if(response.status == 200) {
                $("#onlinebtn").text("Online").removeClass('inactive').addClass('active pulse-blood');
            } else {
                $("#onlinebtn").text("Offline").removeClass('active').addClass('inactive');
            }
        }
    });

});
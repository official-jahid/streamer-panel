$(document).ready(function () {
    console.log('settings loaded - REGIX Studio');
    $.ajax({
        type: "POST",
        url: "/user-info",
        success: function (response) {
            if(response.status == 200) {
                $("#username").text(response.username).addClass('neon-blood');
                $("#hwid").text(response.hwid).addClass('text-red-300');
                $("#expiry").text(response.expiry).addClass('neon-blood');
                $("#onlineusers").text(response.onlineUsers).addClass('text-red-300');
            } else {
                $("#username").text('Not Logged In').addClass('text-red-500');
                $("#hwid").text('---').addClass('text-red-400');
                $("#expiry").text('---').addClass('text-red-400');
                $("#onlineusers").text('---').addClass('text-red-400');
            }
        }
    });
});
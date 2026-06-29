$(document).ready(function () {
    console.log('ready');
    $('input').on('focus', function() {
        $(this).addClass('glow-effect');
    }).on('blur', function() {
        $(this).removeClass('glow-effect');
    });
    $('button').addClass('button-blood');
});
function auth() {
    username = $("#username").val();
    password = $("#password").val();

    SendInfo = {
        username: username,
        password: password
    }

    if(username && password) {
        $("#status").text("Authenticating...").addClass('pulse-blood');
        $.ajax({
            type: "POST",
            url: "/auth",
            data: JSON.stringify(SendInfo),
            contentType: "application/json; charset=utf-8",
            success: function (response) {
                if (response.status == 200) {
                    $("#status").text("Welcome to REGIX Studio!").css('color', '#dc143c');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                } else {
                    $("#status").text("Access Denied!").css('color', '#ff0000').removeClass('pulse-blood');
                }
            },
            error: function() {
                $("#status").text("Connection Error!").css('color', '#ff0000').removeClass('pulse-blood');
            }
        });
    } else {
        $("#status").text("Fill all fields!").css('color', '#ff0000');
    }
}
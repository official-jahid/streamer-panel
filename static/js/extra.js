$(document).ready(function () {
    console.log('extra ready - REGIX Studio');

    $("#chamsmenu").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/chams-menu",
            success: function (response) {
                if(response.status == 200) {
                    $("#chamsmenu").addClass('border-red-500 text-red-300 pulse-blood');
                } else {
                    $("#chamsmenu").addClass('text-red-500');
                }
            }
        });
    });
    
    $("#chams3d").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/chams-3D",
            success: function (response) {
                if(response.status == 200) {
                    $("#chams3d").addClass('border-red-500 text-red-300 pulse-blood');
                } else {
                    $("#chams3d").addClass('text-red-500');
                }
            }
        });
    });

    $("#mbEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/m82b-esp-on",
            success: function (response) {
                if(response.status == 200) {
                    $("#mbEnable").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#mbDisable").removeClass('border-red-500');
                } else {
                    $("#mbEnable").addClass('text-red-500');
                }
            }
        });
    });

    $("#mbDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/m82b-esp-off",
            success: function (response) {
                if(response.status == 200) {
                    $("#mbDisable").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#mbEnable").removeClass('border-red-500');
                } else {
                    $("#mbDisable").addClass('text-red-500');
                }
            }
        });
    });
});
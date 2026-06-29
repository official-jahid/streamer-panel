$(document).ready(function () {
    console.log('Sniper Ready - REGIX Studio');

    $("#ssEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-switch-on",
            success: function (response) {
                if(response.status == 200) {
                    $("#ssEnable").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#ssDisable").removeClass('border-red-500');
                } else {
                    $("#ssEnable").addClass('text-red-500');
                }
            }
        });
    });
    
    $("#ssDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-switch-off",
            success: function (response) {
                if(response.status == 200) {
                    $("#ssDisable").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#ssEnable").removeClass('border-red-500');
                } else {
                    $("#ssDisable").addClass('text-red-500');
                }
            }
        });
    });
    
    $("#swEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-scope-on",
            success: function (response) {
                if(response.status == 200) {
                    $("#swEnable").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#swDisable").removeClass('border-red-500');
                } else {
                    $("#swEnable").addClass('text-red-500');
                }
            }
        });
    });
    
    $("#swDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-scope-off",
            success: function (response) {
                if(response.status == 200) {
                    $("#swDisable").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#swEnable").removeClass('border-red-500');
                } else {
                    $("#swDisable").addClass('text-red-500');
                }
            }
        });
    });
});
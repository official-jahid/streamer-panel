$(document).ready(function () {
    console.log('headshot ready - REGIX Studio');

    $("#aimbotLoad").click(function (e) { 
        e.preventDefault();
        $("#aimbotLoad").addClass("hidden");
        $("#spinner1").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimbot-load",
            success: function (response) {
                if(response.status == 200) {
                    $("#aimbotLoad").addClass('border-red-500 text-red-300 pulse-blood');
                    $("#spinner1").addClass("hidden");
                    $("#aimbotLoad").removeClass("hidden");
                } else {
                    $("#spinner1").addClass("hidden");
                    $("#aimbotLoad").removeClass("hidden");
                    $("#aimbotLoad").addClass('text-red-500');
                }
            }
        });
    });
    
    $("#aimbotEnable").click(function (e) { 
        e.preventDefault();
        $("#aimbotEnable").addClass("hidden");
        $("#aimbotDisable").addClass("hidden");
        $("#spinner2").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimbot-on",
            success: function (response) {
                if(response.status == 200) {
                    $("#spinner2").addClass("hidden");
                    $("#aimbotDisable").removeClass("hidden");
                } else {
                    $("#spinner2").addClass("hidden");
                    $("#aimbotEnable").removeClass("hidden");
                }
            }
        });
        $("#aimbotEnable").removeClass("hidden");
        $("#aimbotDisable").removeClass("hidden");
    });
    
    $("#aimbotDisable").click(function (e) { 
        e.preventDefault();
        $("#spinner2").removeClass("hidden");
        $("#aimbotEnable").addClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimbot-off",
            success: function (response) {
                if(response.status == 200) {
                    $("#spinner2").addClass("hidden");
                    $("#aimbotEnable").removeClass("hidden");
                } else {
                    $("#spinner2").addClass("hidden");
                    $("#aimbotDisable").removeClass("hidden");
                }
            }
        });
    });
    
    $("#dragLoad").click(function (e) { 
        e.preventDefault();
        $("#dragLoad").addClass("hidden");
        $("#spinner3").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimdrag-load",
            success: function (response) {
                if(response.status == 200) {
                    $("#spinner3").addClass("hidden");
                    $("#dragLoad").removeClass("hidden");
                    $("#dragLoad").addClass('border-red-500 text-red-300 pulse-blood');
                } else {
                    $("#spinner3").addClass("hidden");
                    $("#dragLoad").removeClass("hidden");
                    $("#dragLoad").addClass('text-red-500');
                }
            }
        });
    });
    
    $("#dragEnable").click(function (e) { 
        e.preventDefault();
        $("#spinner4").removeClass("hidden");
        $("#dragEnable").addClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimdrag-on",
            success: function (response) {
                if(response.status == 200) {
                    $("#spinner4").addClass("hidden");
                    $("#dragDisable").removeClass("hidden");
                } else {
                    $("#spinner4").addClass("hidden");
                    $("#dragEnable").removeClass("hidden");
                }
            }
        });
    });
    
    $("#dragDisable").click(function (e) { 
        e.preventDefault();
        $("#spinner4").removeClass("hidden");
        $("#dragDisable").addClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimdrag-off",
            success: function (response) {
                if(response.status == 200) {
                    $("#spinner4").addClass("hidden");
                    $("#dragEnable").removeClass("hidden");
                } else {
                    $("#spinner4").addClass("hidden");
                    $("#dragDisable").removeClass("hidden");
                }
            }
        });
    });
});
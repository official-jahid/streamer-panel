$(document).ready(function () {
    console.log('ready');
    var msgbox = false;

    $("#consolebtn").click(function (e) { 
        e.preventDefault();
        msgbox = !msgbox;
        
        if (msgbox) {
            $("#consolebtn").text("Close").addClass('pulse-blood');
            $("#console").toggleClass('hidden').addClass('animate-fadeIn');
            $.ajax({
                type: "POST",
                url: "/logs",
                success: function (response) {
                    if (response.status) {
                        var contents = ""
                        response.message.forEach(element => {
                            var timeStr = element.split(' ')[0] || '';
                            var msgStr = element.substring(9) || element;
                            var content = `<div class="text-red-400 text-sm border-b border-red-800 pb-1 mb-1 animate-pulse"><span class="text-red-500">[${timeStr}]</span> ${msgStr}</div>`;
                            contents += content;
                        });
                        $("#console").html(contents);
                    }
                }
            });
        } else {
            $("#consolebtn").text("Open").removeClass('pulse-blood');
            $("#console").toggleClass('hidden');
        }
    });
});
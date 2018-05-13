$(document).ready(function() {
    var background_element = $('#video_image');
    var do_update_image = true;
    FastClick.attach(document.body);

    function updateBackground(){
        if(!do_update_image){ return; }
        var random = 1 + Math.floor(Math.random() * 10000);
        var img = new Image();
        img.src = image_url + '?' + random;
        img.onload = function(){
            background_element.append(img);
            if (background_element.children().length > 2) {
                $(background_element).find('img:first').remove();
            }
        };
        $(img).addClass('image');
    }

    // check if camera is availabale
    $.get(image_url)
        .done(function(){
            updateBackground();
            setInterval(
                function(){
                    updateBackground();
                }, 2000
            );
        })
        .fail(function(){ do_update_image = false; });

    var code = '';
    function updateMessage(message){
        $('#stars').html(message);
    }

    function refreshCode(){
        updateMessage(Array(code.length + 1).join('*'));
    }
    $('.number').on('click', function(){
        if(!$('#user-name').val()){
            updateMessage('<span class="text">Type Name</span>');
        } else {
            if (code.length < 4) {
                code += $(this).data('nr');
                refreshCode();
            }

            if (code.length === 4) {
                updateMessage('<span class="text">opening ...</span>');
                $.post({
                    url: '/open',
                    data: JSON.stringify({'user': $('#user-name').val(), 'code': code}),
                    dataType: 'json',
                    contentType : 'application/json',
                    success: function(response){
                        if(response.success){
                            updateMessage('<span class="text">' + 'opened'+ '</span>');
                        } else {
                            updateMessage('<span class="error">' + response.error + '</span>');
                        }
                    }
                });
                code = '';
            }
        }
    });

    $('.clear').on('click', function(){
       code = '';
       refreshCode();
    });

});
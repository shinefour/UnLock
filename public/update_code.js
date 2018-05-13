$( document ).ready(function() {
    function updateMessage(message){
        $('#message').html(message);
    }

    $('#update_button').on('click', function(){
        $.ajax({
            async: false,
            type: 'POST',
            url: '/update_code',
            data: JSON.stringify({
                'user': $('#user-name').val(),
                'old_code': $('#old-code').val(),
                'new_code': $('#new-code').val()}),
            dataType: 'json',
            contentType : 'application/json',
            success: function(response){
                if(response.success){
                    updateMessage('<span class="text">Success</span>');
                } else {
                    updateMessage('<span class="error">' + response.error + '</span>');
                }
            }
        });
    });

});
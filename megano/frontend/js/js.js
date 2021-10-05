function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(".ProductCard-cartElement .btn").click(function(e){
    e.preventDefault();
    var qty = $('[name="amount"]').val();
    var id_product = $('[name="amount"]').data('id');

        $.ajax({
            type: 'POST',
            url: '/cart/add/'+id_product+'/',
            headers: {
                'X-CSRFToken':getCookie('csrftoken')
            },
            data: {'count': qty},
            mode: 'same-origin',
            dataType: 'json',
            context: $(this),
            success: function (data) {
                if (data.code == 200) {
                    var $item = $('<div class="message">' + data.message + '</div>');
                    $item.appendTo($('.message-box')).delay(3000).slideUp(200, function(){
                        $item.remove();
                    });
                }
                console.log(data);
                /* иначе пересчитать корзину*/
            },
            error: function (xhr, ajaxOptions, thrownError) {
               console.log(thrownError);
               console.log(ajaxOptions);
               console.log(xhr);
              }
        }

    );
 });
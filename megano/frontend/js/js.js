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
function show_message(message){
    const $item = $('<div class="message">' + message+ '</div>');
    $item.appendTo($('.message-box')).delay(3000).slideUp(200, function(){
        $item.remove();
    });
}
function ajax_request(url, data, success_func, type='POST'){
    $.ajax({
                type: type,
                url: url,
                headers: {
                    'X-CSRFToken':getCookie('csrftoken')
                },
                data: data,
                mode: 'same-origin',
                dataType: 'json',
                success: function (data) {success_func(data)},
                error: function (xhr, ajaxOptions, thrownError) {
                   console.log(thrownError);
                   console.log(ajaxOptions);
                   console.log(xhr);
                  }
            });
}


function cart_update(id_product, data){
    ajax_request(
            '/cart/update/'+id_product+'/',
            data,
            function (res){
                show_message(res.message)
                $('.amount-sum').text(res.amount_sum);
                $('.amount-count').text(res.amount_count);
            });
}


$(document).ready(function(){
    /* удаление товара из корзины*/
    $("#cart-area").on('click', '.Cart-delete', function(e){
        e.preventDefault();
        let id_product = $(this).parent().parent().find('[name="amount"]').data('id')
        let elem = $(this).parent().parent().parent();

        ajax_request(
            '/cart/update/'+id_product+'/',
            false,
            function (res){
                show_message(res.message)
                elem.remove();
                $('.amount-sum').text(res.amount_sum);
                $('.amount-count').text(res.amount_count);
            },
            'DELETE'
        );
    });

    /* Добавление товара детальная */
    $(".ProductCard-cartElement .btn").click(function(e){
        e.preventDefault();
        let id_product = $('[name="amount"]').data('id');
        let qty = $('[name="amount"]').val();
        cart_update(id_product, {'count': qty});
     });
    /* Добавление товара каталог */
    $(".Card-btn").click(function(e){
        e.preventDefault();
        let id_product = $(this).data('id');
        let qty = 1;
        cart_update(id_product, {'count': qty});
     });


    /* Добавление товара */
    $('#cart-area .Amount-remove, #cart-area .Amount-add').click(function(e){
        e.preventDefault();
        let id_product = $(this).parent().find('[name="amount"]').data('id');
        let qty = $(this).parent().find('[name="amount"]').val();
        cart_update(id_product, {'count': qty, 'update': true});

     });
    $('#cart-area .Amount-input').change(function(e){
        e.preventDefault();

        let id_product = $(this).data('id');
        let qty = $(this).val();
        console.log(qty);
        if (qty!=''){
            cart_update(id_product, {'count': qty, 'update': true});
        }else {
            $(this).val(0)
        }
     });


});
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
$(document).ready(function (){
     $(".Tabs-addComment form").submit(function(e){
         e.preventDefault()
          $.ajax({
              type: 'POST',
              data: $(this).serialize(),
              url: "add_comment/",
              headers: {
                        'X-CSRFToken':getCookie('csrftoken')
                    },
              success: function (response) {
                  $('.msg').text('Комментарий успешно опубликован');
              },
               error: function (res) {
                       console.log(res);
                       $('.msg').text(res.responseText);
                      }
          });
     });
})
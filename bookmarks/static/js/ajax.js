var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function () {
    $('a.follow').click(function (e) {
        e.preventDefault();
        $.post('{% url "user_follow" %}',
            {
                id: $(this).data('id'),
                action: $(this).data('action')
            },
            function (data) {
                if (data['status'] == 'ok') {
                    let previous_action = $('a.follow').data('action');

                    // toggle data-action
                    $('a.follow').data('action', previous_action == 'follow' ? 'unfollow' : 'follow');

                    // toggle link text
                    $('a.follow').text(previous_action == 'follow' ? 'Unfollow' : 'Follow');

                    // update total followers
                    let previous_followers = parseInt($('span.count .total').text());
                    $('span.count .total').text(previous_action == 'follow' ? previous_followers + 1 : previous_followers - 1);
                }
            }
        );
    });
});

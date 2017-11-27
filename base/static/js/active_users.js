$(document).ready(function() {
  var link = $('#online-users > div.online-users');
  var arrow = $('#online-users > div.online-users > span.pull-right > i');
  var users = $('#online-users > div.box-event-content.online');

  // this function changes the arrow icon in online-users div with a click
  var changeButtonArrow = function() {
    if (arrow.hasClass('fa-chevron-up')) {
      arrow.removeClass('fa-chevron-up');
      arrow.addClass('fa-chevron-down');
    } else {
      arrow.removeClass('fa-chevron-down');
      arrow.addClass('fa-chevron-up');
    }
  };

  // this function show/hide users in online-users div, also call changeButtonArrow
  link.click(function(event) {
    event.preventDefault();
    users.slideToggle(200, changeButtonArrow);
  });

  $('select.user-search').select2({
    ajax: {
      url: '/api/v1/users/?status=1&search_only_by_name=1',
      dataType: 'json',
      delay: 250,
      cache: true,

      processResults: function(data) {
        var i;
        var user;
        var results = [];
        for (i = 0; i < data.users.length; i += 1) {
          user = data.users[i];
          var text = user.get_full_name;
          results.push({
            id: user.pk,
            text: text
          });
        }

        return {
          results: results
        };
      }
    }
  });
});

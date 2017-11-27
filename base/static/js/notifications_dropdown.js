$(document).ready(function() {

  setInterval(function() {
    var url = window.location.href;
    url = url.split('/')[0] + '/notifications/last/';

    //Every 60 seconds we to check notifications on a server
    $.ajax({
      url: url,
      success: function(response) {
        $('#notifications-dropdown + .dropdown-menu.notifications').remove();
        $('#notifications-dropdown').replaceWith($(response));
      }
    });
  }, 60000);

});

$(document).ready(function() {

  //Changing the filter select box updates the view
  $('.apply-filter-select').val($('input[name="o"]').val()).trigger('change');
  $('.apply-filter-select').change(function() {
    var request_path = $('input[name="request_path"]').val();
    var q = '?q=' + $('input[name="q"]').val();
    var url = request_path + q;

    if (this.value !== '') {
      url += '&o_=' + this.value;
    }

    window.location = url;
  });

  //Click on load more button sends a request to a server to retrieve more methodologies
  //We track the number of a current page which is sent to a server
  var currentPage = 1;
  $('a.load-more-btn').click(function() {
    currentPage++;
    $.ajax({
      url: window.location.href,
      data: {
        p: currentPage
      },
      success: function(response) {
        $('.methodology-list').append($(response));
        //If it is the last page, the load more button is removed from DOM
        if (currentPage >= $('a.load-more-btn').data('pages')) {
          $('a.load-more-btn').remove();
        }
      }
    });
  });

  //Handling sending a share request
  $('a.confirm-share-btn').click(function() {
    //If no users are selected the warning becomes temporarily visible
    if (!$('select.user-search').val()) {
      blinkAlert($('.no-users-alert'));
      return;
    }

    //Show loading sign
    $('.fa-cog').show();

    //Server request
    $('form.share-form').ajaxSubmit({
      url:  window.location.href + 'share/',
      type: 'POST',
      success: function(response) {
        //Hide loading sign
        $('.fa-cog').hide();

        //If server sends us an error (it can happen inside the success request)
        //we also temporarily show a warning. Otherwise we close the modal
        if (response.status === 'error') {
          blinkAlert($('.server-error-alert'));
        } else {
          $('.share-modal').modal('toggle');
        }
      },

      error: function() {
        //Show warning and hide the loading sign
        $('.fa-cog').hide();
        blinkAlert($('.server-error-alert'));
      }
    });

    function blinkAlert($alert) {
      $alert.show();
      setTimeout(function() {$alert.hide();}, 5000);
    }
  });

  //Handling clicking on download button if a user is not logged in
  $('a.login-to-download').click(function() {
    swal('Para poder ver este documento debes solicitar acceso a "estadoinnovador@lab.gob.cl"');
  });
});

$(document).ready(function() {
  if (!$('.email_messages').length) {
    return;
  }

  $('.user-search').change(function() {
    window.location = '/messages/u/' + this.value;
  });

  //Scrolling to the bottom
  var $msgPanel = $('.messages-exchange');
  $msgPanel.scrollTop($msgPanel.prop('scrollHeight'));
  var msgHeight = $msgPanel.prop('scrollHeight');
  $msgPanel.scrollTop(msgHeight);

  //Emulating ajax-request when user scrolls to the top
  $msgPanel.scroll(function() {
    if ($(this).scrollTop() === 0) {
      loadOldMessages();
    }
  });

  //Every 30 seconds we check if our interlocutor has just written something
  setInterval(function() { loadNewMessages(); }, 10000);

  //On Enviar click we send a message to a server anf then load new messages
  $('.send-message-btn').click(function() {
    var url = '/messages/new/';
    $('form.write-message').ajaxSubmit({
      url: url,
      type: 'post',
      success: function(response) {
        loadNewMessages(true);
      }
    });

    $('form.write-message').trigger('reset');
  });

  function loadNewMessages(scrollToBottom) {
    var firstMessageId = $msgPanel.find('.message').last().data('id');
    $.ajax({
      url: window.location.href,
      data: {
        'id__gt': firstMessageId
      },
      success: function(response) {
        if (response) {

          //Removing no messages div
          $msgPanel.find('.no-messages-message').remove();

          //Removing a date
          response = response.replace(/\<h4 class="text-center"\>.*?\<\/h4\>/, '');
          $msgPanel.append(response);

          if (scrollToBottom) {
            $msgPanel.scrollTop($msgPanel.prop('scrollHeight'));
          }
        }
      }
    });
  }

  function loadOldMessages() {
    var $lastMessageDiv = $msgPanel.find('.message').first();
    var lastMessageId = $lastMessageDiv.data('id');
    app.utils.showLoading();
    $.ajax({
      url: window.location.href,
      data: {
        'id__lt': lastMessageId
      },
      success: function(response) {
        //Removing the obsolete date div
        if (response !== '') {
          var $firstDateBeforeLoad =  $msgPanel.find('h4.text-center').first();

          $msgPanel.prepend(response);

          var $lastDateInLoad = $firstDateBeforeLoad.
            prevAll('h4.text-center').first();

          if ($firstDateBeforeLoad && $lastDateInLoad &&
            $firstDateBeforeLoad.text() === $lastDateInLoad.text()) {

            $firstDateBeforeLoad.remove();
          }

            app.utils.hideLoading();
            $msgPanel.animate({scrollTop: $lastMessageDiv.position().top}, 200)
        } else {
          app.utils.hideLoading();
        }
      }
    });
  }

});

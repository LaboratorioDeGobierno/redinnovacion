/* globals Dropzone, app, _ */

$(document).ready(function() {
  var commentContentSelector = '.comment-content p';

  var commentDropzone;
  if (window.Dropzone) {
    var $commentDropzone = $('#commentDropzone');

    if ($commentDropzone.length) {

      Dropzone.options.commentDropzone = false;
      commentDropzone = new Dropzone('#commentDropzone', {
        url: $('#commentDropzone').data('action'),
        dictDefaultMessage: 'Agrega fotos a tu publicación',
        headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
        maxFilesize: 2, // MB
        paramName: 'image', // The name that will be used to transfer the file

        init: function() {
          this.on('success', function(file, response) {
            var $option = $(
              '<option selected value="' + response.id + '"></option>'
            );
            $('#id_images').append($option);
          });
        }
      });
    }
  }

  // Embedder ---------------------------------------------------------------
  $.extend(window.Embedder.defaultOptions, {
    oEmbedEndpoint: '/api/v1/oembed/',
    vimeoWidth: 390,
    vimeoHeight: 220
  });

  /*
   * Returns a common handler to append embed responses after `$object`.
   */
  function videoEmbed($object) {
    return function(result) {
      var html = (
        '<div class="embed-responsive embed-responsive-16by9">' +
        result.html + '</div>'
      );
      $($object).after($(html));
    };
  }

  /*
   * Iterate through comments within 'scope' to get their text and run the
   * embedding parser. If no 'scope' is passed it will search in the entire
   * document.
   */
  function initEmbedder(scope) {
    var $scope = (typeof (scope) === 'undefined') ? $(document) : $(scope);
    $scope.find(commentContentSelector).each(function() {
      var $this = $(this);

      try {
        window.Embedder({
          text: $this.text(),
          youtubeCallback: videoEmbed($this),
          vimeoCallback: videoEmbed($this)
        });
      }
      catch (e) {
        //Just to prevent the app from completely dying
      }
    });
  }

  // Search for embeddable content on page start
  initEmbedder();

  // Comment mentions -------------------------------------------------------
  var mentionUsers; // pseudo-global that stores user's information
  var cachedMentionUsers = {}; // pseudo-global that stores user's information
  var cachedMentionUsersByName = {}; // pseudo-global that stores user's information

  /*
   * Runs $.fn.mention over comment forms within 'scope' if no 'scope' is
   * passed it will search in the entire document.
   *
   * Also parsers comments and replace mentions with html link.
   */
  function initMentions(scope) {
    var $scope = (typeof (scope) === 'undefined') ? $(document) : scope;

    var commentFormSelector = 'textarea';
    var commentMentionsSelector = '.comment-mentions';
    var delimiter = '@';

    // Initialize $.fn.mention
    $scope.find(commentFormSelector).mention({
      sensitivity: true,
      delimeter: delimiter,
      users: mentionUsers,
      typeaheadOpts: {
        afterSelect: function() {
          var val = this.$menu.find('.active').attr('data-value');
          var $option = this.$element.closest('form').find(
            commentMentionsSelector + ' option[data-match="' + val + '"]'
          );
          $option.prop('selected', true);
        }
      }
    });

    // Replace mentions with html link.
    $scope.find(commentContentSelector).each(function() {
      var $this = $(this);
      var text = $this.text();
      var matches = text.match(new RegExp(delimiter + '\\d+', 'g'));
      if (matches === null || matches === undefined) {
        return;
      }

      $.each(matches, function(_, match) {
        var html = $this.html();
        var idUser = match.substring(delimiter.length);
        var user = cachedMentionUsers[idUser];
        if (user === undefined) {
          return;
        }

        var link = (
          '<a href="' + user.url + '">' + delimiter + user.username +
          '</a>'
        );
        html = html.replace(match, link);
        $this.html(html);
      });
    });

    setTimeout(function() {
      var $commentMentionsSelector = $scope.find(commentMentionsSelector);
      var options = '';

      function addUserOption(_, user) {
        options += '<option value="' + user.id + '" data-match="' +
          user.username + '">' + user.username + '</option>';
      }

      // prepare options string
      $.each(mentionUsers, addUserOption);

      // Add options to comment-mentions forms
      $commentMentionsSelector.append(options);

    }, 100);

  }

  // Receive users information from server and initialize mention on the
  // entire document.
  $.getJSON('/api/v1/users/mentionables').then(function(json) {
    mentionUsers = json.users;
    $.each(mentionUsers, function() {
      cachedMentionUsers[this.id] = this;
      cachedMentionUsersByName[this.username] = this;
    });

    initMentions();
  });

  // highlight button ------------------------------------------------------------
  function highlightButtonClick() {
    var $btn = $(this);
    var commentId = $btn.data('comment-id');

    $.ajax({
      type: 'post',
      url: '/comments/' + commentId + '/highlight/',
      data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },

      dataType: 'json',
      error: function(response, textStatus, errorThrown) {
        if (response.status == 422) {
          handleInvalidForm(response.responseJSON);
        }
      },

      success: function(data) {
        if (data.highlighted) {
          $btn.addClass('highlighted').removeClass('active');
        } else {
          $btn.removeClass('highlighted').removeClass('active');
        }
      }
    });
  }

  $('.comment-highlight-btn').click(highlightButtonClick);

  // Like button ------------------------------------------------------------
  function likeButtonClick() {
    var $btn = $(this);
    var commentId = $btn.data('comment-id');

    $.ajax({
      type: 'post',
      url: '/comments/likes/create/',
      data: {
        comment: commentId,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },

      dataType: 'json',
      error: function(response, textStatus, errorThrown) {
        if (response.status == 422) {
          handleInvalidForm(response.responseJSON);
        }
      },

      success: function(data) {
        var quantity = parseInt($btn.find('.quantity').text()) + 1;
        $btn.find('.quantity').text(quantity);
        $btn.addClass('liked').removeClass('active').unbind('click');
      }
    });
  }

  $('.comment-like-btn').click(likeButtonClick);

  // Load more button --------------------------------------------------------
  function loadMoreComments() {
    var $btn = $(this);
    var updatedAt = $btn.data('updated-at');
    var eventId = $btn.data('event-id');
    var authorId = $btn.data('author-id');

    app.utils.showLoading();
    $.ajax({
      data: {
        authorId: authorId,
        updatedAt: updatedAt,
        eventId: eventId
      },
      error: function(response, textStatus, errorThrown) {
        console.log(response);
        app.utils.hideLoading();
      },

      success: function(data) {
        var $data = $(data);
        $btn.closest('.load-more-space').replaceWith($data);
        $data.find('.comment-load-more-btn').click(loadMoreComments);
        $data.find('.comment-like-btn').click(likeButtonClick);
        $data.find('.comment-highlight-btn').click(highlightButtonClick);
        initEmbedder($data);
        initMentions($data);
        app.utils.hideLoading();
      },

      url: '/comments/'
    });
  }

  $('.comment-load-more-btn').click(loadMoreComments);

  // Handle comment submit ---------------------------------------------------
  $('#comment-form').submit(function(e) {
    e.preventDefault();
    var $form = $(this);
    var text = $form.find('textarea').val();

    // can't submit a empty text
    if (!text) {
      alert('El comentario no puede ser vacío.');
      return;
    }

    $.ajax({
      data: $form.serialize(),
      error: function(response, textStatus, errorThrown) {
        if (response.status == 422) {
          handleInvalidForm(response.responseJSON);
        }
      },

      success: function(data) {
        if (commentDropzone) {
          commentDropzone.removeAllFiles();
        }

        var $commentContent = $(data);

        $('.comment-list').prepend($commentContent);
        initCounter($commentContent.find('textarea')[0]);

        $form[0].reset();
        $form.find('textarea').val('');
        $form.find('select[name="images"]').find('option').remove();
        $form.find('select[name="user_mentions"]').find('option').attr(
          'selected', false);

        var $commentsCount = $('.comments-count');
        $commentsCount.html(parseInt($commentsCount.html()) + 1);

        var $comment = $('.comment-list .comment').first();

        $comment.find('.comment-gallery').lightGallery({
          selector: '.comment-image'
        });

        initEmbedder($comment);
        initMentions($comment);

        $comment.find('.comment-highlight-btn').click(highlightButtonClick);
        $comment.find('.comment-like-btn').click(likeButtonClick);
      },

      type: $form.attr('method'),
      url: $form.attr('action')
    });
  });

  $(document).on('click', '.comment-answer-btn', function() {
    var $this = $(this);
    var $input = $this.closest('.collapse').find('form textarea[name="text"]');
    var text = '@' + $this.data('user') + ', ';
    $input.text(text);
    $input.focus();
  });

  $('.comment-gallery').lightGallery({ selector: '.comment-image' });

  // transform mention_id in mention_username in text edit
  $(document).on('click', '.comment-edit', function() {
    var $this = $(this);
    var $textarea = $('textarea' + $this.attr('href'));
    var text = $textarea.text();
    var delimiter = '@';

    var matches = text.match(new RegExp(delimiter + '\\d+', 'g'));
    if (matches === null || matches === undefined) {
      return;
    }

    // check any match in textarea
    $.each(matches, function(_, match) {
      var html = $textarea.html();
      var idUser = match.substring(delimiter.length);
      var user = cachedMentionUsers[idUser];
      if (user === undefined) {
        return;
      }

      var userMention = (
        '' + delimiter + user.username
      );

      html = html.replace(match, userMention);

      // update html textarea
      $textarea.html(html);
    });
  });

  // replace all mentions_username with mentions_ids
  $(document).on('submit', '.edit-form', function(e) {
    e.preventDefault();
    var $form = $(this);
    var text = $form.find('textarea').val();

    // can't submit a empty text
    if (!text) {
      alert('El comentario no puede ser vacío.');
      return;
    }

    var delimiter = '@';

    // find mention matches
    var matches = text.match(
      new RegExp(delimiter + '[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', 'g')
    );

    var data = {};
    $.each($form.serializeArray(), function() {
      data[this.name] = this.value;
    });

    if (!(matches === null || matches === undefined)) {
      // check any match in textarea
      $.each(matches, function(_, match) {
        var text = data.text;
        var username = match.substring(delimiter.length);
        var user = cachedMentionUsersByName[username];
        if (user === undefined) {
          return;
        }

        var userTagId = (
          '' + delimiter + user.id
        );
        data.text = text.replace(match, userTagId);
      });
    }

    // delete None elements
    for (var key in data) {
      if (data[key] === 'None') {
        delete data[key];
      }
    }

    // send ajax request to edit comment
    $.ajax({
      data: data,
      error: function(response, textStatus, errorThrown) {
        if (response.status == 422) {
          handleInvalidForm(response.responseJSON);
        }
      },

      success: function(data) {
        // add html to comment list
        var $commentContent = $(data);
        $('.comment-list').prepend($commentContent);

        // hide edit form
        $form.closest($('.comment')).hide();
        $form[0].reset();
        $form.find('textarea').val('');

        // update mentions
        var $comment = $('.comment-list .comment').first();
        initEmbedder($comment);
        initMentions($comment);
      },

      type: $form.attr('method'),
      url: $form.attr('action')
    });
  });

  $(document).on('submit', '.comment-answer', function(e) {
    e.preventDefault();
    var $form = $(this);
    var text = $form.find('textarea').val();

    // can't submit a empty text
    if (!text) {
      alert('La respuesta no puede ser vacía.');
      return;
    }

    var delimiter = '@';

    // find mention matches
    var matches = text.match(
      new RegExp(delimiter + '[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', 'g')
    );
    if (matches === null || matches === undefined) {
      matches = [];
    }

    var data = {};
    $.each($form.serializeArray(), function() {
      data[this.name] = this.value;
    });

    // check any match in textarea
    $.each(matches, function(_, match) {
      var text = data.text;
      var username = match.substring(delimiter.length);
      var user = cachedMentionUsersByName[username];
      if (user === undefined) {
        return;
      }

      var userTagDd = (
        '' + delimiter + user.id
      );
      data.text = text.replace(match, userTagDd);
    });

    // send ajax request to edit comment
    $.ajax({
      data: data,
      error: function(response, textStatus, errorThrown) {
        if (response.status == 422) {
          handleInvalidForm(response.responseJSON);
        }
      },

      success: function(data) {
        // add html to comment list
        var $commentContent = $(data);
        $commentContent.insertAfter($form);

        // hide edit form
        $form[0].reset();
        $form.find('textarea').text('');

        // update mentions
        var $comment = $('.comment-answer-list .comment').first();
        initEmbedder($comment);
        initMentions($comment);
      },

      type: $form.attr('method'),
      url: $form.attr('action')
    });
  });
});

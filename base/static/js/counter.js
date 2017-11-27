$(document).ready(function() {

  //HOTFIX: removing counters from modal dialogs
  //TODO: They should not be generated first of all
  $('.modal .counter').remove();

  var inputSelector = 'input[maxlength],textarea[maxlength]';
  var excludeSelectors = '.modal input, .modal textarea';

  window.initCounter = function(el) {
    var $input = $(el);
    var max = $input.attr('maxlength');

    if (!max) {
      console.log('no maxlength attribute');
      return;
    }

    var $counter = $(
      '<span class="counter pull-right" data-limit="' + max + '">' +
      max +
      '</span>'
    );
    $input.after($counter);

    startCounter($counter[0]);
    $input.bind('input', bindInput);
  };

  function bindInput() {
    var $input = $(this);
    var $counter = $input.siblings('.counter');
    var curLength = $input.val().length;
    var maxLength = $counter.data('limit');

    if (curLength >= maxLength) {
      var input =   $input.val();
      $input.val(input.substr(0, maxLength));
      curLength = maxLength;

      $counter.addClass('blink-text');
      setTimeout(function() {
        $counter.removeClass('blink-text');
      }, 500);
    } else {
      checkCounterVerticalPosition($counter, $input);
    }

    $counter.text(curLength + '/' + maxLength);
  }

  $(inputSelector).not(excludeSelectors).each(function(ind, el) {
    initCounter(el);
  });

  $(window).resize(function() {
    $('.counter').each(function(ind, el) {
      positionCounter(el);
    });
  });

  function startCounter(counter) {
    positionCounter(counter);
    var textLen = $(counter).siblings('input, textarea').val().length;
    $(counter).text(textLen + '/' + $(counter).data('limit'));
  }

  function positionCounter(counter) {
    $(counter).after('<div class="clearfix"></div>');
  }

  function checkCounterVerticalPosition($counter, $element) {
    var normalPositionFlag = !$counter.hasClass('down');
    var curLength = $element.val().length;
    var width = $element.width();

    //Empirical value
    var charsInLine = width / 9;

    if (curLength >= charsInLine && normalPositionFlag) {
      $counter.addClass('down');
      var inputHeight = $element.outerHeight();
      $counter.animate({top: '+=' + inputHeight + 'px'}, 200);
    } else if (curLength < charsInLine && !normalPositionFlag) {
      $counter.removeClass('down');
      var inputHeight = $element.outerHeight();
      $counter.animate({top: '-=' + inputHeight + 'px'}, 200);
    }
  }
});

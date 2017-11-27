(function() {
  'use strict';


  $('.rating-star').on('click', function () {
    const $element = $(this).closest('.rating');
    const $container = $(this).closest('.rating-stars');
    const $visualValue = $container.find('.rating-quantity label');
    const $input = $container.find('.rating-quantity .value input');
    const value = $element.data('value');

    //clear state
    for (var i = 1; i <= 5; i++) {
      $container.find('.star-'+i).removeClass('active');
    }

    $element.toggleClass('active');
    const state = $element.hasClass('active');

    for (var i = 1; i < value; i++) {
      const $star = $container.find('.star-'+i);
      if (state) {
        $star.addClass('active');
      } else {
        $star.removeClass('active');
      }
    }

    $visualValue.html('(' + value + ')');
    $input.val(value);

  });

  $('.rating-quantity .value input').each(function() {
    const $container = $(this).closest('.rating-stars');
    const value = parseInt($(this).val());

    //clear state
    for (var i = 1; i <= 5; i++) {
      $container.find('.star-' + i).removeClass('active');
    }

    for (var i = 1; i <= value; i++) {
      const $star = $container.find('.star-' + i);
      $star.addClass('active');
    }
  });

})();

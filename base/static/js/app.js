var App = {};
var app;

(function() {
  app = {
    data: {},
    messages: {},
    forms: {
      datepicker: {
        format: 'dd/mm/yyyy',
        language: 'es',
        autoclose: true
      },
      dateTimePicker: {
        language: 'es'
      }
    }
  };

  app.utils = {
    hideLoading: function() {
      $('body').removeClass('wait');
    },

    thousandSeparator: function(x) {
      x = Math.round(x);
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    },

    showLoading: function() {
      $('body').addClass('wait');
    },

    highlight: function($el) {
      $el.addClass('highlight');
      setTimeout(function() {
        $el.toggleClass('dim highlight');
      }, 15);
      setTimeout(function() {$el.removeClass('dim');}, 1010);
    }
  };

  $('.mt-checkbox-span').click(function() {
    var $parent = $(this).closest('.mt-checkbox');
    var $checkbox = $parent.find('input[type="checkbox"]').first();
    $checkbox.prop('checked', !$checkbox.prop('checked'));
    $(this).toggleClass('green');
  });

  $('.mt-checkbox').each(function () {
    var $checkbox = $(this).find('input[type="checkbox"]').first();
    if ($checkbox.prop('checked')) {
      $(this).find('.mt-checkbox-span').addClass('green');
    }
  });

  $('.cancel-interest').click(function() {
    $(this).parent().remove()
  })
  $( ".form-interest" ).change(function() {
    $(".interest").append( "<span class='label label-default'>"+$(this).val()+" <a class='cancel-interest'><i class='fa fa-times'></i></a></span>" );
    $('.cancel-interest').click(function() {
      $(this).parent().remove()
    })
  });

  $('.hidden').hide().removeClass('hidden');
  var active=false;
  $('.navbar-toggle').click(function() {
    if (active){
      $('.header-line-select').css("background", "none")
      active=false;
    }else{
      $('.header-line-select').css("background", "#fff")
      active=true;
    }
  });

  var availableTags = [
     "ActionScript",
      "AppleScript",
       "Asp",
  ];
  $( ".search" ).keydown(function() {
    var value = $(this).val();
    if (value.length >= 0){
        var link="/api/v1/institutions/?q="+value
        $.ajax({
          url: link,
          data: {},
          dataType: "json",
          cache: false,
          success: function(data) {
                $('.institutions').html(jade['institutions/item']({'institutions':data.institutions}))
                $('.institutions-mobile').html(jade['institutions/item_mobile']({'institutions':data.institutions}))
                return false;
          },
          error: function(jqXHR, textStatus, errorThrown) {
              if (errorThrown!="")  alert(errorThrown+' : '+textStatus);
          },
          crossDomain: false,
          type: "GET",
      })
    }

  });

  $('.alert').each(function() {
    app.utils.highlight($(this));
  });
  $('.datetime-picker').datetimepicker({
    icons: {
      previous: 'fa fa-angle-left',
      next: 'fa fa-angle-right',
      time: 'fa fa-clock-o',
      up: 'fa fa-chevron-up',
      down: 'fa fa-chevron-down',
      date: 'fa fa-calendar',
    },
    format: 'DD/MM/YYYY HH:mm'
  });

  $('.popover-toggle').popover().click(function() {
    $(this).popover('hide');
  });
}());

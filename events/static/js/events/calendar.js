(function() {
  'use strict';

  var $calendar = $('#calendar');
  $calendar.fullCalendar({
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'month,agendaWeek,agendaDay'
    },
    defaultView: 'month',
    timeFormat: 'HH:mm',
    firstDay: 1,
    axisFormat: 'HH:mm',
    scrollTime: '08:00:00',
    editable: false,
    selectable: false,
    selectHelper: false,
    eventRender: function(event, element, view) {
      element.addClass('event-type-' + event.type);

      const $element = $(
        'td[data-date="' + moment(event.start).format('YYYY-MM-DD') + '"]'
      ).first();
      if ($element.hasClass('fc-past')) {
        element.addClass('fc-past');
      }

      if ($element.hasClass('fc-today')) {
        element.addClass('fc-today');
      }

      if ($element.hasClass('fc-future')) {
        element.addClass('fc-future');
      }
    },

    eventLimit: true,
    eventClick: function(calEvent, jsEvent, view) {

      var $calendar = $('#calendar');
      var $currentTarget = $(jsEvent.currentTarget);
      var $eventView = $('#event-view').css({top: 0, left: 0});

      var place = [calEvent.county, calEvent.region]
        .filter(Boolean).join(', ');

      var containerCoord = $calendar.offset();
      var elementCoord = $currentTarget.offset();
      var coord = {
        top: elementCoord.top - containerCoord.top,
        left: elementCoord.left - containerCoord.left
      };

      // right side;
      if (($calendar.width() / 2) < coord.left) {
        coord.left = coord.left - ($eventView.outerWidth() - $currentTarget.outerWidth());
      }

      $eventView
        .removeClass(function (index, className) {
          return (className.match (/(^|\s)event-type-\S+/g) || []).join(' ');
        })
        .addClass('show-event')
        .addClass('event-type-' + calEvent.type)
        .css(coord);
      $('#event-title').html(calEvent.title);
      $('#event-place').html(place);
      $('#event-time').html(calEvent.startStr + ' - ' + calEvent.endStr);
      $('#event-link').prop('href', calEvent.eventUrl);

      var $eventApply = $('#event-apply');

      if (calEvent.registerUrl && calEvent.type !== 'experimenta') {
        $eventApply.prop('href', calEvent.registerUrl);
        $eventApply.show();
      } else {
        $eventApply.prop('href', '');
        $eventApply.hide();
      }

    },

    events: {
      url: '/events/calendar/data',
      data: function() { // a function that returns an object
        var hideWorkshops = !$('input[name=workshops]:checked').prop('checked');
        hideWorkshops = hideWorkshops || '';

        var hideMeetings = !$('input[name=meetings]:checked').prop('checked');
        hideMeetings = hideMeetings || '';

        var data = {
          region: $('input[name=region]:checked').val(),
          hideEvents: !$('input[name=events]:checked').prop('checked') || '',
          hideWorkshops: hideWorkshops,
          hideMeetings: hideMeetings,
          hideTalks: !$('input[name=talks]:checked').prop('checked') || '',
          hideExternal: !$('input[name=external]:checked').prop('checked') || '',
          hideExperimenta: !$('input[name=experimenta]:checked').prop('checked') || ''
        };

        return data;
      }
    }
  });

  $('input[name=region]').change(function() {
    $calendar.fullCalendar('refetchEvents');
    $('.region-name').html($(this).closest('label').text());
  });

  $('.calendar-filters input[type=checkbox]').change(function() {
    $calendar.fullCalendar('refetchEvents');
  });

  $('.panel-close').on('click', function () {
    $(this).closest('#event-view').removeClass('show-event');
  })

})();

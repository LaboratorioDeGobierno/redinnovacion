$(document).ready(function() {
  // get graph div
  var ctx = $('#region-chart').get(0).getContext('2d');

  // set data arrays
  var labels = [];
  var colors = [];
  var _data = [];

  // get info from html
  $('.region-bullet').slice(0, 3).each(function() {
    colors.push($(this).find('i').css('color'));
    labels.push($($(this).find('span')[0]).text());
    _data.push($($(this).find('span.count')).text());
  });

  // get info from html
  var others = $('.region-bullet.others');
  colors.push(others.find('i').css('color'));
  labels.push($(others.find('span')[0]).text());
  _data.push($(others.find('span.count')).text());

  // set graph config
  var data = {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Usuarios',
          backgroundColor: colors,
          data: _data
        }
      ]
    },
    options: {
      cutoutPercentage: 80,
      legend: {
        display: false
      }
    }
  };

  // create graph
  var myNewChart = new Chart(ctx, data);

  // show hidden regions in regions list
  $('.show-all-regions').click(function() {
    $('.region-bullet').slideDown();
    $('.region-bullet.others').hide();
    $('.show-all-regions').hide();
    $('.hide-some-regions').show();
  });

  // hide non-top regions in regions list
  $('.hide-some-regions').click(function() {
    $('.region-bullet').slice(3).slideUp();
    $('.region-bullet.others').show();
    $('.hide-some-regions').hide();
    $('.show-all-regions').show();
  });
});

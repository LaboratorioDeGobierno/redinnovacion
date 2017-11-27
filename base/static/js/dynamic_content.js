$(document).ready(function() {
  var $videos = $('iframe.video');
  $.each($videos, function(i, v) {
    var src = $(v).attr('src');

    //Wrapping youtube links
    src = src.replace(/youtube.com\/watch\?v=(.*?)/, 'youtube.com/embed/$1');

    //Wrapping vimeo links
    src = src.replace(/vimeo.com\/(.*?)/, 'player.vimeo.com/video/$1');

    $(v).attr('src', src);
  });
});

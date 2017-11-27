$(document).ready(function() {
  $('#id_content').summernote({
    height: 220,
    callbacks: {
      onChange: function(contents, $editable) {
        $('.overlay-caption').html(contents);
        $('.content-content').html(contents);
      }
    }
  });

  var $photosDropzoneForm = $('.photos-gallery');
  var $imageDropzoneForm = $('.image-gallery');

  var $videoGroup = $('#id_url').closest('.form-group');
  var $htmlGroup = $('.note-editor').closest('.form-group');
  var $gallery = $('.gallery');

  var $textAreaHint = $('.textarea-hint');

  updateView();
  $('#id_kind').change(updateView);

  function updateView() {
    var kind = $('#id_kind').val();
    $videoGroup.hide();
    $htmlGroup.hide();
    $gallery.hide();
    $textAreaHint.hide();
    if (kind === 'video') {
      $videoGroup.show();
      $htmlGroup.show();
    } else if (kind === 'html') {
      $htmlGroup.show();
    } else if (kind === 'gallery') {
      $gallery.show();
      $photosDropzoneForm.show();
      $imageDropzoneForm.hide();
    } else if (kind === 'image') {
      $htmlGroup.show();
      $gallery.show();
      $photosDropzoneForm.hide();
      $imageDropzoneForm.show();
      $textAreaHint.show();
    }
  }
});

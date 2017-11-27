$(document).ready(function() {

  function success() {
    var $dynamicContentPreview = $('#dynamic-content-preview');
    $.ajax({
      url: $dynamicContentPreview.data('url'),
      success: function(response) {
        $dynamicContentPreview.html(response);
        $('.overlay-caption').html($('#id_content').val());
      }
    });
  }

  function getRemovedFile(model) {
    return function(file) {
      var _ref = file.previewElement;
      var obj = JSON.parse(file.xhr.response);
      $.ajax({
        method: 'DELETE',
        url: '/comments/' + model + '/' + obj.id + '/delete/',
        headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
        success: function() {
          if (_ref !== null || _ref !== undefined) {
            return _ref.parentNode.removeChild(file.previewElement);
          }
        }
      });
    }
  }

  Dropzone.options.photosDropzone = {
    maxFilesize: 30, // MB
    addRemoveLinks: true,
    removedfile: getRemovedFile('photos'),
    success: success,
    dictRemoveFile: 'Eliminar'
  };

  Dropzone.options.imageDropzone = {
    maxFilesize: 30, // MB
    addRemoveLinks: true,
    dictRemoveFile: 'Eliminar',
    maxFiles: 1,
    success: success,
    maxfilesexceeded: function(file) {
      this.removeAllFiles();
      this.addFile(file);
    }
  };


  Dropzone.options.filesDropzone = {
    maxFilesize: 100, // MB
    addRemoveLinks: true,
    removedfile: getRemovedFile('files'),
    success: success,
    dictRemoveFile: 'Eliminar'
  };

  $('.delete-btn').click(function() {
    $this = $(this);
    $.ajax({
      method: 'DELETE',
      url: $this.data('url'),
      headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
      success: function() {
        $this.closest('.uploaded-item').remove();
      }
    });
  });
});

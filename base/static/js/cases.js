$(document).ready(function() {

  Dropzone.options.filesDropzone = {
    maxFilesize: 100, // MB
    addRemoveLinks: true,
    dictRemoveFile: 'Eliminar'
  };

  $('.delete-btn').click(function() {
    var $this = $(this);
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

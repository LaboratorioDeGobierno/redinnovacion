// HACK: everything

$(document).ready(function() {
  var cropper;
  var avatarInputSelector = '#id_avatar';

  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        $('.user-avatar-lg').attr(
          'style',
          'background-image: url("' + e.target.result + '");'
        );

        if (cropper) {
          cropper.replace(e.target.result);
        }
      };

      reader.readAsDataURL(input.files[0]);
    }
  }

  $(avatarInputSelector).change(function() {
    readURL(this);
  });

  $(avatarInputSelector).find('a').remove();

  if (window.Cropper) {
    var image = document.getElementById('cropper-img');
    if (!image) {
      return;
    }

    cropper = new Cropper(image, {
      aspectRatio: 1,
      viewMode: 2,
      autoCropArea: 1,
      minCropBoxWidth: 150
    });

    $('.cropper-save').click(function() {
      var $this = $(this);
      $(this).addClass('disabled');
      $(this).append('<i class="fa fa-spinner fa-pulse fa-fw"></i>');
      var canvas =  cropper.getCroppedCanvas();
      var onBlobReady = function(blob) {
        var formData = new FormData();
        var key = $('input[name=csrfmiddlewaretoken]').val();
        formData.append('avatar', blob);
        formData.append('csrfmiddlewaretoken', key);
        $.ajax({
          url: $this.data('url'),
          method: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function() {
            window.location.reload();
          },

          error: function() {
            console.error('Upload error');
          }
        });
      };

      canvas.toBlob(onBlobReady, 'image/jpeg', 0.8);
    });

    $('.nav.nav-tabs > li > a').on('shown.bs.tab', function() {
      cropper.onResize();
    });
  }
});

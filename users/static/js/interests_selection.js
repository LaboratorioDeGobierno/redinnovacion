(function() {
  var otherInterestSelector = '#other-topics-checkbox';
  var otherInterestFieldSelector = '#id_1-other_topics';
  var formGroupSelector = '.form-group';

  function main() {
    $(otherInterestSelector).on('change', function(e) {
      $field = $(otherInterestFieldSelector).closest(formGroupSelector);
      if (e.target.checked) {
        $field.show();
      } else {
        $(otherInterestSelector).val('');
        $field.hide();
      }
    });
  }

  $(document).ready(main);
}());

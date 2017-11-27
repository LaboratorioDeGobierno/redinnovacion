(function() {
  var institutionSelector = '#id_0-institution, #id_institution';
  var otherInstitutionSelector = (
    '#id_0-other_institution_name, #id_other_institution_name'
  );
  var formGroupSelector = '.form-group';
  var otherValue = '';

  function main() {
    $(institutionSelector).on('change', function() {
      $field = $(otherInstitutionSelector).closest(formGroupSelector);
      if ($(this).val() === otherValue) {
        $field.show();
      } else {
        $(otherInstitutionSelector).val('');
        $field.hide();
      }
    });

    $(institutionSelector).change();
  }

  $(document).ready(main);
}());

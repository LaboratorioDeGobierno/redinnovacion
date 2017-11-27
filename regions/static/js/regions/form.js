(function() {
  'use strict';

  // selectors
  var regionSelector = '.form-group-region select, #id_region';
  var countySelector = '.form-group-county select, #id_county';

  function getCounties(regionValue) {
    $(countySelector).each(function() {
      var $this = $(this);
      $this.select2({
        ajax: {
          url: '/api/v1/counties/?region=' + regionValue,
          cache: true,
          delay: 250,
          data: function(params) {
            return {
              name: params.term
            };
          },

          processResults: function(data) {
            var i;
            var county;
            var results = [];
            for (i = 0; i < data.length; i += 1) {
              county = data[i];
              results.push({
                id: county.pk,
                text: county.name
              });
            }

            return {
              results: results
            };
          }
        }
      });
    });
  }

  $(regionSelector).on('change', function() {
    var regionValue = $('option:selected', this).val();
    $(countySelector).val('');
    getCounties(regionValue);
  });

  getCounties($(regionSelector).find('option:selected').val());
}());

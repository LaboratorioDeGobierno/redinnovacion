(function() {
  function toggleTabs() {
    $('.toggle-tabs').on('change', function() {
      $('#nav-tabs li a').eq($(this).val()).tab('show');
    });
  }

  $(document).ready(toggleTabs);
})();

jQuery(document).ready(function ($) {
  var $j = jQuery.noConflict();
  $j.ajax({
    type: "GET",
    url: "/ict/asset_type/",
    success: function (data) {
      $("#asset_type").html(data);
    },
    error: function (error) {
      alert("Select Asset Type!!!");
    },
  });

  $j.ajax({
    type: "GET",
    url: "/ict/region/",
    success: function (data) {
      $("#region").html(data);
    },
    error: function (error) {
      alert("Select Region!!!");
    },
  });

  $("#region").change(function () {
    var RegionId = $(this).val();

    $j.ajax({
      type: "GET",
      url: "/ict/station/",
      data: {
        RegionId: RegionId,
      },
      success: function (data) {
        $("#station").html(data);
      },
      error: function (error) {
        alert("Select Region!!!");
      },
    });
  });
});

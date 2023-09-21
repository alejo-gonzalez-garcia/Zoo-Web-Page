function on_click_card() {
  $(".click").off("click").on("click", function (e) {
    e.preventDefault();

    if ($(this).hasClass("link-to-modal")) {
      $(".modal-body").load($(this).attr("href"), function () {
        on_click_card();
        $("#modalView").modal("show");
      });
    } else {
      if ($(this).attr("href")) {
        window.location.href = $(this).attr("href");
      }
    }
  });
}

$(document).ready(function () {
  on_click_card();
});

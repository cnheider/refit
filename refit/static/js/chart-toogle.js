$(function () {
  $('#toggle-steps').change(function () {
    toogleOff("#linecom.google.step_count.delta")
  });
})

function toogleOff(id) {
  console.log(id);
  $("#linecom.google.step_count.delta").css('display', 'none')
}

function toogleOn(id) {
  $(id).css('display', 'block')
}

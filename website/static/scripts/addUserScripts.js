$("#access").on('change', (e) => {
  if (e.target.value == 'User') {
    $("#signup-mpk-box").show()
  } else {
    $("#signup-mpk-box").hide()
    $("#signup-mpk").val(null)
  }
})

$("#add-mpk").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-mpk").removeClass('add-button')
    $("#add-mpk").addClass('cancel-button')
    $("#signup-new-mpk").show()

  } else {
    $("#add-mpk").removeClass('cancel-button')
    $("#add-mpk").addClass('add-button')
    $("#signup-new-mpk").hide()
    $("#signup-new-mpk").val(null)
  }
})

$("#signup-button").on('click', (e) => {
  checkedCount = 0;
  $("#mpk-list li input").each(function () {
    if ($(this).is(":checked")) {
      checkedCount++;
    }
  })
  access = $("#access").val()
  new_mpk = $("#signup-new-mpk").val()
  console.log($("#access").val())
  if (checkedCount == 0 && access == 'User' && new_mpk == '') {
    e.preventDefault()
    $("#mpk-alert").show()
  }
});
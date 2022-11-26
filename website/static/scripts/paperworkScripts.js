$("#add-mpk").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-mpk").removeClass('add-button')
    $("#add-mpk").addClass('cancel-button')
    $("#nowy_mpk").show()
    $("#select-mpk").hide()
  } else {
    $("#add-mpk").removeClass('cancel-button')
    $("#add-mpk").addClass('add-button')
    $("#nowy_mpk").hide()
    $("#nowy_mpk").val(null)
    $("#select-mpk").show()
  }
})


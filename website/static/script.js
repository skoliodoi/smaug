
$('#rent_hardware').on("change", () => {
  $("#rent_hardware_container").toggle()
});


$('#add_paperwork').on("change", () => {
  $("#add_paperwork_container").toggle()
})

$("#hardware_container").on("click", () => {
  console.log('Up')
  $("#hardware_details").css("display", "block")
  $("#paperwork_details").css("display", "none")
}
)
$("#paperwork_container").on("click", () => {
  console.log('Up')
  $("#hardware_details").css("display", "none")
  $("#paperwork_details").css("display", "block")
})

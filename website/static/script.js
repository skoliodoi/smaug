function sayHello() {
  console.log('Hello world')
}

$('#rent_hardware').on("change", () => {
  $("#rent_hardware_container").toggle()
})


$('#add_paperwork').on("change", () => {
  console.log('Click')
  $("#add_paperwork_container").toggle()
})

$('#multiple_select')
  .dropdown()
  ;

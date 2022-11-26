const table = $('#all_items_table').DataTable(
  {
    dom: 'lfrt<"#table-bottom-container" <"#table-bottom-left" i B> p>',
    buttons: {
      buttons: ['csv', 'excel']
    }
  }
);

$("#items-filter").on('change', (e) => {
  if (e.target.value == 'all') {
    window.location.href = '/hardware/all'
  } else {
    window.location.href = `/hardware/get_data/${e.target.value}`
  }
})

$("#paperwork-filter").on('change', (e) => {
  if (e.target.value == 'all') {
    window.location.href = '/paperwork/all'
  } else {
    window.location.href = `/paperwork/get_data/${e.target.value}`
  }
})





$('#add_paperwork').on("change", () => {
  $("#add_paperwork_container").toggle()
})

$("#hardware_container").on("click", () => {
  $("#hardware_details").show()
  $("#rental_details").hide()
  $("#paperwork_details").hide()
}
)
$("#rental_container").on("click", () => {
  $("#rental_details").show()
  $("#paperwork_details").hide()
  $("#hardware_details").hide()
}
)
$("#paperwork_container").on("click", () => {
  $("#paperwork_details").show()
  $("#rental_details").hide()
  $("#hardware_details").hide()
})






$("#zwrot-uwagi-btn").on('click', () => {
  $("#zwrot-uwagi-btn").hide();
  $("#cancel-uwagi-btn").show();
  $("#cancel-uwagi-btn").attr({ "style": "cursor: pointer" });
  $("#zwrot-uwagi").show()
})

$("#cancel-uwagi-btn").on('click', () => {
  $("#cancel-uwagi-btn").hide();
  $("#zwrot-uwagi-btn").show();
  $("#zwrot-uwagi-btn").attr({ "style": "cursor: pointer" });
  $("#zwrot-uwagi").hide()
  $("#opis-uszkodzenia").val(null)
  $("#zwrot-dodatkowe-uwagi").val(null)
  $("#opis-uszkodzenia-box").hide()
  $("#zwrot-stan option:selected").prop('selected', false)
})


$("#zwrot-stan").on('change', (e) => {
  if (e.target.value != "Sprawny") {
    $("#opis-uszkodzenia-box").show()
  } else {
    $("#opis-uszkodzenia-box").hide()
    $("#opis-uszkodzenia").val(null)
  }

})

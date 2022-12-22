$('#rent_hardware').on("change", () => {
  $('#rent_hardware').is(':checked') ? $("#rent-hardware-bool").prop("checked", true) : $("#rent-hardware-bool").prop("checked", false);
  $("#rent_hardware_container").toggle()
  $("#hardware_container").toggle()
  $("#dodaj-plik").toggle()
  let isChecked = $('#rent_hardware').is(":checked")
  if (!isChecked) {
    $("#login").val(null)
    $("#login").removeAttr('required')
    $("#mocarz_id").val(null)
    $("#nowy_projekt").val(null)
    $("#nowy_projekt").hide()
    $("#cancel-projekt").hide()
    $("#select-projekt").show()
    $("#select-projekt").removeAttr('required')
    $("#nowa_lokalizacja").val(null)
    $("#nowa_lokalizacja").hide()
    $("#cancel-lokalizacja").hide()
    $("#select-lokalizacja").show()
    $("#select-lokalizacja").removeAttr('required')
    $("#select-projekt option:selected").prop('selected', false)
    $("#select-lokalizacja option:selected").prop('selected', false)
    $("#sluchawki option:selected").prop('selected', false)
    $("#zlacze option:selected").prop('selected', false)
    $("#przejsciowka option:selected").prop('selected', false)
    $("#mysz option:selected").prop('selected', false)
    $("#torba option:selected").prop('selected', false)
    $("#modem option:selected").prop('selected', false)
    $("#karta-zblizeniowa option:selected").prop('selected', false)
    $("#notatki-wypozyczenie").val(null)
  } else {
    $("#login").attr('required', true)
    $("#select-projekt").attr('required', true)
    $("#select-lokalizacja").attr('required', true)
  }
}
);

$(function () {
  initialStan = $("#select-stan").val();
  if (initialStan == 'Sprawny') {
    $("#opis-uszkodzenia").hide()
  } else {
    $("#opis-uszkodzenia").show()
  }
});

/*Dodawanie nowych elementw do listy*/

// $("#select-stanowisko").on('change', (e) => {
//   if (e.target.value == 'DODAJ') {
//     $("#cancel-stanowisko").show()
//     $("#nowy_stanowisko").show()
//     $("#select-stanowisko").hide()
//   }
// })

$("#add-stanowisko").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-stanowisko").removeClass('add-button')
    $("#add-stanowisko").addClass('cancel-button')
    $("#nowy_stanowisko").show()
    $("#select-stanowisko").hide()
    $("#select-stanowisko").val(null)
  } else {
    $("#add-stanowisko").removeClass('cancel-button')
    $("#add-stanowisko").addClass('add-button')
    $("#nowy_stanowisko").hide()
    $("#nowy_stanowisko").val(null)
    $("#select-stanowisko").show()
  }
})
$("#add-typ").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-typ").removeClass('add-button')
    $("#add-typ").addClass('cancel-button')
    $("#nowy_typ").show()
    $("#select-typ").hide()
    $("#select-typ").removeAttr('required')
    $("#select-typ").val(null)
  } else {
    $("#add-typ").removeClass('cancel-button')
    $("#add-typ").addClass('add-button')
    $("#nowy_typ").hide()
    $("#nowy_typ").val(null)
    $("#select-typ").show()
    $("#select-typ").attr('required', true)
  }
})
$("#add-marka").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-marka").removeClass('add-button')
    $("#add-marka").addClass('cancel-button')
    $("#nowa_marka").show()
    $("#select-marka").hide()
    $("#select-marka").removeAttr('required')
    $("#select-marka").val(null)
  } else {
    $("#add-marka").removeClass('cancel-button')
    $("#add-marka").addClass('add-button')
    $("#nowa_marka").hide()
    $("#nowa_marka").val(null)
    $("#select-marka").show()
    $("#select-marka").attr('required', true)
  }
})
$("#add-model").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-model").removeClass('add-button')
    $("#add-model").addClass('cancel-button')
    $("#nowy_model").show()
    $("#select-model").hide()
    $("#select-model").removeAttr('required')
    $("#select-model").val(null)
  } else {
    $("#add-model").removeClass('cancel-button')
    $("#add-model").addClass('add-button')
    $("#nowy_model").hide()
    $("#nowy_model").val(null)
    $("#select-model").show()
    $("#select-model").attr('required', true)
  }
})
$("#add-projekt").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-projekt").removeClass('add-button')
    $("#add-projekt").addClass('cancel-button')
    $("#nowy_projekt").show()
    $("#select-projekt").hide()
    $("#select-projekt").removeAttr('required')
    $("#select-projekt").val(null)
  } else {
    $("#add-projekt").removeClass('cancel-button')
    $("#add-projekt").addClass('add-button')
    $("#nowy_projekt").hide()
    $("#nowy_projekt").val(null)
    $("#select-projekt").show()
    $("#select-projekt").attr('required', true)
  }
})
$("#add-system").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-system").removeClass('add-button')
    $("#add-system").addClass('cancel-button')
    $("#nowy_system").show()
    $("#select-system").hide()
    $("#select-system").removeAttr('required')
    $("#select-system").val(null)
  } else {
    $("#add-system").removeClass('cancel-button')
    $("#add-system").addClass('add-button')
    $("#nowy_system").hide()
    $("#nowy_system").val(null)
    $("#select-system").show()
    $("#select-system").attr('required', true)
  }
})
$("#add-mpk").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-mpk").removeClass('add-button')
    $("#add-mpk").addClass('cancel-button')
    $("#nowy_mpk").show()
    $("#select-mpk").hide()
    $("#select-mpk").removeAttr('required')
    $("#select-mpk").val(null)
  } else {
    $("#add-mpk").removeClass('cancel-button')
    $("#add-mpk").addClass('add-button')
    $("#nowy_mpk").hide()
    $("#nowy_mpk").val(null)
    $("#select-mpk").show()
    $("#select-mpk").attr('required', true)
  }
})
$("#add-lokalizacja").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-lokalizacja").removeClass('add-button')
    $("#add-lokalizacja").addClass('cancel-button')
    $("#nowa_lokalizacja").show()
    $("#select-lokalizacja").hide()
    $("#select-lokalizacja").removeAttr('required')
    $("#select-lokalizacja").val(null)
  } else {
    $("#add-lokalizacja").removeClass('cancel-button')
    $("#add-lokalizacja").addClass('add-button')
    $("#nowa_lokalizacja").hide()
    $("#nowa_lokalizacja").val(null)
    $("#select-lokalizacja").show()
    $("#select-lokalizacja").attr('required', true)
  }
})
$("#add-sluchawki").on('click', (e) => {
  const classes = e.currentTarget.classList;
  if (Array.from(classes).includes("add-button")) {
    $("#add-sluchawki").removeClass('add-button')
    $("#add-sluchawki").addClass('cancel-button')
    $("#nowe_sluchawki").show()
    $("#select-sluchawki").hide()
    $("#select-sluchawki").val(null)
  } else {
    $("#add-sluchawki").removeClass('cancel-button')
    $("#add-sluchawki").addClass('add-button')
    $("#nowe_sluchawki").hide()
    $("#nowe_sluchawki").val(null)
    $("#select-sluchawki").show()
    $("#select-sluchawki").val('Nie dotyczy')
  }
})



// $("#select-typ").on('change', (e) => {
//   if (e.target.value == 'DODAJ') {
//     $("#cancel-typ").show()
//     $("#nowy_typ").show()
//     $("#select-typ").hide()
//   }
// })


// $("#select-marka").on('change', (e) => {
//   if (e.target.value == 'DODAJ') {
//     $("#cancel-marka").show()
//     $("#nowa_marka").show()
//     $("#select-marka").hide()
//   }
// })

// $("#select-model").on('change', (e) => {
//   if (e.target.value == 'DODAJ') {
//     $("#cancel-model").show()
//     $("#nowy_model").show()
//     $("#select-model").hide()
//   }
// })

$("#select-stan").on('change', (e) => {
  if (e.target.value == 'Sprawny') {
    $("#opis-uszkodzenia").hide()
    $("#opis-uszkodzenia-input").val(null)
  } else {
    $("#opis-uszkodzenia").show()
  }
})



// $("#select-projekt").on('change', (e) => {
//   if (e.target.value == 'DODAJ') {
//     $("#cancel-projekt").show()
//     $("#nowy_projekt").show()
//     $("#select-projekt").hide()
//   }
// })

// $("#select-lokalizacja").on('change', (e) => {
//   if (e.target.value == 'DODAJ') {
//     $("#cancel-lokalizacja").show()
//     $("#nowa_lokalizacja").show()
//     $("#select-lokalizacja").hide()
//   }
// })


/*Anuluj dodawanie*/
$("#cancel-stanowisko").on('click', () => {
  $("#cancel-stanowisko").hide()
  $("#nowy_stanowisko").hide()
  $("#nowy_stanowisko").val(null)
  $("#select-stanowisko option:selected").prop('selected', false)
  $("#select-stanowisko").show()
})
$("#cancel-typ").on('click', () => {
  $("#cancel-typ").hide()
  $("#nowy_typ").hide()
  $("#nowy_typ").val(null)
  $("#select-typ option:selected").prop('selected', false)
  $("#select-typ").show()
})
$("#cancel-marka").on('click', () => {
  $("#cancel-marka").hide()
  $("#nowa_marka").hide()
  $("#nowa_marka").val(null)
  $("#select-marka option:selected").prop('selected', false)
  $("#select-marka").show()
})
$("#cancel-model").on('click', () => {
  $("#cancel-model").hide()
  $("#nowy_model").hide()
  $("#nowy_model").val(null)
  $("#select-model option:selected").prop('selected', false)
  $("#select-model").show()
})
$("#cancel-projekt").on('click', () => {
  $("#cancel-projekt").hide()
  $("#nowy_projekt").hide()
  $("#nowy_projekt").val(null)
  $("#select-projekt option:selected").prop('selected', false)
  $("#select-projekt").show()
})
$("#cancel-lokalizacja").on('click', () => {
  $("#cancel-lokalizacja").hide()
  $("#nowa_lokalizacja").hide()
  $("#nowa_lokalizacja").val(null)
  $("#select-lokalizacja option:selected").prop('selected', false)
  $("#select-lokalizacja").show()
})
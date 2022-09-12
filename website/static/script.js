
$('#rent_hardware').on("change", () => {
  $("#rent_hardware_container").toggle()
  $("#hardware_container").toggle()
  $("#dodaj-plik").toggle()
  let isChecked = $('#rent_hardware').is(":checked")
  if (isChecked == false) {
    $("#mocarz_id").val(null)
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
  }
});

$("#select-typ").on('change', (e) => {
  if (e.target.value == 'DODAJ') {
    $("#cancel-typ").show()
    $("#nowy_typ").show()
  } else {
    $("#cancel-typ").hide()
    $("#nowy_typ").hide()
    $("#nowy_typ").val(null)
  }
})

$("#select-stan").on('change', (e) => {
  if (e.target.value == 'Sprawny') {
    $("#opis-uszkodzenia").hide()
    $("#opis-uszkodzenia-input").val(null)
  } else {
    $("#opis-uszkodzenia").show()
  }
})

// $(document).load(function () {
//   alert($("#select-stan").val());
// });

$(function () {
  initialStan = $("#select-stan").val();
  if (initialStan == 'Sprawny') {
    $("#opis-uszkodzenia").hide()
  } else {
    $("#opis-uszkodzenia").show()
  }
});

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

// $("#zagrozenie_submit").on('click', (e) => {
//   e.preventDefault()
//   const miejscowosc = $("#zagrozenie_miejscowosc").val()
//   const gmina = $("#zagrozenie_gmina").val()
//   const ulica = $("#zagrozenie_ulica").val()
//   const nrDomu = $("#zagrozenie_dom").val()
//   const kodPocztowy = $("#zagrozenie_kod").val()
//   const nazwiskoFirma = $("#zagrozenie_nazwisko_firma").val()
//   const telefon = $("#zagrozenie_telefon").val()
//   const opis = $("#zagrozenie_opis").val()
//   const koronawirus = $("#zagrozenie_koronawirus").val()
//   const stanNapiecia = $("input[name='napiecie']:checked", "#zagrozenie_form").val()
//   $.post("/erz-zagrozenie", {
//     "miejscowosc": miejscowosc,
//     'gmina': gmina,
//     'ulica': ulica,
//     'nr_budynku': nrDomu,
//     'kod_pocztowy': kodPocztowy,
//     'nazwisko_firma': nazwiskoFirma,
//     'telefon': telefon,
//     'opis': opis,
//     'koronawirus': koronawirus,
//     'napiecie': stanNapiecia
//   }).done(data => {
//     window.location.href = `/success/${data}`
//   })

// })

// const options = ['Test', 'Test2', 'Test3']

// $("div.toolbar").html(`<select id="table-select"></select>`);

// $('#table-select').on('click', () => {
//   alert('clicked')
// })

$("#select-marka").on('change', (e) => {
  if (e.target.value == 'DODAJ') {
    $("#cancel-marka").show()
    $("#nowa_marka").show()
  } else {
    $("#cancel-marka").hide()
    $("#nowa_marka").hide()
    $("#nowa_marka").val(null)
  }
})

$("#select-model").on('change', (e) => {
  if (e.target.value == 'DODAJ') {
    $("#cancel-model").show()
    $("#nowy_model").show()
  } else {
    $("#cancel-model").hide()
    $("#nowy_model").hide()
    $("#nowy_model").val(null)
  }
})

$("#select-projekt").on('change', (e) => {
  if (e.target.value == 'DODAJ') {
    $("#cancel-projekt").show()
    $("#nowy_projekt").show()
  } else {
    $("#cancel-projekt").hide()
    $("#nowy_projekt").hide()
    $("#nowy_projekt").val(null)
  }
})

$("#select-lokalizacja").on('change', (e) => {
  if (e.target.value == 'DODAJ') {
    $("#cancel-lokalizacja").show()
    $("#nowa_lokalizacja").show()
  } else {
    $("#cancel-lokalizacja").hide()
    $("#nowa_lokalizacja").hide()
    $("#nowa_lokalizacja").val(null)
  }
})

$("#cancel-typ").on('click', () => {
  $("#cancel-typ").hide()
  $("#nowy_typ").hide()
  $("#nowy_typ").val(null)
  $("#select-typ option:selected").prop('selected', false)
})
$("#cancel-marka").on('click', () => {
  $("#cancel-marka").hide()
  $("#nowa_marka").hide()
  $("#nowa_marka").val(null)
  $("#select-marka option:selected").prop('selected', false)
})
$("#cancel-model").on('click', () => {
  $("#cancel-model").hide()
  $("#nowy_model").hide()
  $("#nowy_model").val(null)
  $("#select-model option:selected").prop('selected', false)
})
$("#cancel-projekt").on('click', () => {
  $("#cancel-projekt").hide()
  $("#nowy_projekt").hide()
  $("#nowy_projekt").val(null)
  $("#select-projekt option:selected").prop('selected', false)
})
$("#cancel-lokalizacja").on('click', () => {
  $("#cancel-lokalizacja").hide()
  $("#nowa_lokalizacja").hide()
  $("#nowa_lokalizacja").val(null)
  $("#select-lokalizacja option:selected").prop('selected', false)
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

$("#access").on('change', (e) => {
  console.log(e.target.value)
  if (e.target.value == 'All') {
    $("#access-box").removeClass('lg:col-span-6')
    $("#access").addClass('lg:col-span-3')
    $("#signup-mpk").show()
  } else {
    $("#signup-mpk").remove()
  }
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

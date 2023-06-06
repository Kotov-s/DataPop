jQuery(document).ready(function () {
  var columnsSelect = jQuery('#columns');
  var columnsSelectInitialized = false;
  window.scrollTo(0, document.body.scrollHeight);


  checkSelectedOption(columnsSelect, columnsSelectInitialized);

  jQuery('#analysis-options').change(function () {
    checkSelectedOption(columnsSelect, columnsSelectInitialized);
  });
});


function rebuildSelect(myArray, selectDiv, isDisabled, numnberOfOptions) {
  const remove = $('#select .bootstrap-select');
  $(remove).replaceWith($(remove).contents('.selectpicker'));
  $('.selectpicker').selectpicker();

  const newSelect = document.createElement('select');
  newSelect.id = 'columns';

  newSelect.setAttribute('data-max-options', numnberOfOptions);

  newSelect.setAttribute('multiple', '');
  newSelect.setAttribute('name', 'columns');
  newSelect.setAttribute('data-live-search', 'true');
  newSelect.setAttribute('title', 'Выберите строку');
  newSelect.classList.add('shadow', 'selectpicker', 'form-control');
  newSelect.disabled = isDisabled;

  myArray.forEach((value) => {
    const newOption = document.createElement('option');
    newOption.value = value.toString();
    newOption.textContent = value.toString();
    newSelect.appendChild(newOption);
  });

  selectDiv.appendChild(newSelect);
  $('.selectpicker').selectpicker();
  isDisabled = !isDisabled;
}


function checkSelectedOption() {
  const myArray = columns;
  const selectDiv = document.querySelector('#select');
  var analysisOption = $("#analysis-options").val();
  var selectedOptionId = $('#analysis-options option:selected').attr('id');
  if (selectedOptionId === 'columns-analysis') {
    if (analysisOption == 'delete_column') {
      rebuildSelect(myArray, selectDiv, false, '10');
    }
    else {
      rebuildSelect(myArray, selectDiv, false, '1');
    }
    
    showAlert('Выберите колонку для анализа', 'primary');
  }


  else if (selectedOptionId === '2-columns-analysis') {

    if (analysisOption == 'state_map_plot') {
      showAlert('Выберите колонку с штатами и колонку для анализа.', 'primary', 4);
    }

    rebuildSelect(myArray, selectDiv, false, '2');


    showAlert('Выберите колонки для анализа', 'primary');
  }
  else {
    rebuildSelect(myArray, selectDiv, true, '0');

  }
}


function showAlert(message, color, multiplier = 1) {
  var alertEl = document.createElement("div");
  alertEl.className = "toast align-items-center border-0 fade show mt-5 fixed-top ms-auto text-bg-" + color + " mx-4";
  alertEl.setAttribute("role", "alert");
  alertEl.setAttribute("aria-live", "assertive");
  alertEl.setAttribute("aria-atomic", "true");
  alertEl.innerHTML = '<div class="d-flex"><div class="toast-body">' + message + '</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>';

  document.body.appendChild(alertEl);

  setTimeout(function () {
    alertEl.remove();
  }, 1500 * multiplier);
}


function sendAjaxRequest(analysisOption, columnName) {
  $.ajax({
    type: "POST",
    url: `/chat/${analysisOption}`,
    data: {
      "threadId": threadId,
      "columnName[]": columnName,
      "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function (data) {
      // В случае успеха, мы перезагружаем страницу, 
      // чтобы добавить новые сообщения и удалить старые столбцы из списка
      window.location.reload();
    },
    error: function (error) {
      showAlert('Произошла ошибка: ' + error, 'danger');
    }
  });
}

$("#my-form").submit(function (e) {
  e.preventDefault();
  var selectedOptionId = $('#analysis-options option:selected').attr('id');
  var analysisOption = $("#analysis-options").val();
  // columnName = $("#columns").val();
  const selectedOptions = document.querySelectorAll('#columns option:checked');
  const values = Array.from(selectedOptions).map(option => option.value);
  const newValues = values.filter(value => !prevSelections.includes(value));
  console.log(newValues);

  prevSelections = values;

  checkSelectedOption(jQuery('#columns'), false);

  if (selectedOptionId === 'full-analysis') {
    sendAjaxRequest(analysisOption, newValues);
  }
  else if (selectedOptionId === 'columns-analysis' && newValues.length) {
    sendAjaxRequest(analysisOption, newValues);
  }

  else if (selectedOptionId === '2-columns-analysis' && newValues.length == 2) {
    if (analysisOption == 'state_map_plot') {
      showAlert('Убедителсь, что вы выбрали колонку с штатами.\nСоздание изображения может занять около минуты', 'primary');
    }
    sendAjaxRequest(analysisOption, newValues);
  }


  // Если выбран анализ колонки, но колонка не выбрана
  else if (selectedOptionId === 'columns-analysis' && newValues.length === 0) {
    showAlert('Вы не выбрали колонку для исследования', 'danger');
  }


  else if (selectedOptionId === '2-columns-analysis' && newValues.length !== 2) {
    showAlert('Вы не выбрали две колонки для исследования', 'danger');
  }
});





// function updateColumns() {
//   return new Promise(function (resolve, reject) {
//     $.ajax({
//       type: "POST",
//       url: `/chat/columns`,
//       data: {
//         "threadId": threadId,
//         "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
//       },
//       success: function (data) {
//         var cols = data.columns;
//         resolve(cols);
//       },
//       error: function (error) {
//         reject(error);
//       }
//     });
//   });
// }


        // var selectElement = $('select[name=columns]');
        // console.log($('select[name=columns]'));

        // // Remove previous options and li elements
        // selectElement.empty();
        // console.log($('#bs-select-2 ul'));
        // $('#bs-select-2 ul').empty();

        // for (var i = 0; i < cols.length; i++) {
        //   col_name = cols[i];
        //   selectElement.append('<option value=' + col_name + '>' + col_name + '</option>');
        //   $('#bs-select-2 ul').append('<li><a role="option" class="dropdown-item" id="bs-select-2-' + i + '" tabindex="0"><span class="text">' + col_name + '</span></a></li>');
        // }
        // $('#bs-select-2 ul').empty();
        // selectElement.prop('disabled', false);
        // selectElement.selectpicker('refresh');


// function createMessage(data) {

//   var message = document.createElement("div");
//   message.classList.add("bg-white", "rounded", "p-3", "mx-3", "shadow", "mb-3", "overflow-auto", "mx-auto");

//   // Создаем заголовок
//   var header = document.createElement("p");
//   header.classList.add("h4");
//   header.innerText = data.title;
//   message.appendChild(header);

//   if (data.enable) {
//     var explanation = document.createElement("div");
//     explanation.classList.add("alert", "alert-light", "font-monospace");
//     explanation.innerHTML = data.explanation;
//     message.appendChild(explanation);
//   }

//   // Добавляем содержимое сообщения
//   var content = document.createElement("div");
//   content.innerHTML = data.html;
//   message.appendChild(content);

//   var messageContainer = document.querySelector("#message-container");
//   messageContainer.appendChild(message);

//   window.scrollTo(0, document.body.scrollHeight);
//   window.location.reload();
// }
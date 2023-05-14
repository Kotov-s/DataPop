jQuery(document).ready(function () {
  var selectedOptionId = $('#analysis-options option:selected').attr('id');
  if (selectedOptionId === 'columns-analysis') {
    updateColumns();
  }
  else {
    $('select[name=columns]').prop('disabled', true);
    $('select[name=columns]').selectpicker('refresh');
  }

  jQuery('#analysis-options').change(function () {
    updateColumns();
  });
});


$("#my-form").submit(function (e) {
  e.preventDefault();

  var selectedOptionId = $('#analysis-options option:selected').attr('id');
  var analysisOption = $("#analysis-options").val();
  var columnName = $("#columns").val();

  if (selectedOptionId === 'full-analysis') {
    columnName = "";
    $.ajax({
      type: "POST",
      url: `/chat/${analysisOption}`,
      data: {
        "threadId": threadId,
        "columnName": columnName,
        "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (data) {
        createMessage(data);
      },
      error: function (error) {
        alert("An error occurred: " + error);
      }
    });
  }
  else if (columnName) {

    $.ajax({
      type: "POST",
      url: `/chat/${analysisOption}`,
      data: {
        "threadId": threadId,
        "columnName": columnName,
        "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (data) {
        createMessage(data);
      },
      error: function (error) {
        alert("An error occurred: " + error);
      }

    });
    // Если мы удалили колонку, то удалить ее из селекта
    if (analysisOption == 'delete_column') {
      var optionToRemove = $(`select[name=columns] option[value="${columnName}"]`);
      optionToRemove.remove();
      $('select[name=columns]').selectpicker('refresh');
    }

  }

  else {
    // Если выбран пункт с работой для колонки, но не выбрана сама колонка, то показать предупреждение
    var alertEl = document.createElement("div");
    alertEl.className = "alert d-flex align-items-center fixed-top w-25 rounded-5 m-4 ms-auto alert-danger";
    alertEl.setAttribute("role", "alert");
    alertEl.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16" role="img" aria-label="Warning:"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"></path></svg><div>Вы не выбрали колонку для исследования</div>';

    document.body.appendChild(alertEl);

    setTimeout(function () {
      alertEl.remove();
    }, 1500);
  }

});

function updateColumns() {

  var selectedOptionId = $('#analysis-options option:selected').attr('id');
  var analysisOption = $("#analysis-options").val();
  if (selectedOptionId === 'columns-analysis') {
    $.ajax({
      type: "POST",
      url: `/chat/columns`,
      data: {
        "threadId": threadId,
        "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (data) {
        cols = data.columns;
        console.log(cols);
        var selectElement = $('select[name=columns]');
        selectElement.empty(); // remove old options
        for (var i = 0; i < cols.length; i++) {
          col_name = cols[i];
          selectElement.append('<option value=' + col_name + '>' + col_name + '</option>');
        }
        selectElement.prop('disabled', false);
        selectElement.selectpicker('refresh');
      },
      error: function (error) {
        alert("An error occurred: " + error);
      }
    });
  }
  else {
    $('select[name=columns]').prop('disabled', true);
    $('select[name=columns]').selectpicker('refresh');
  }
}


function createMessage(data) {

  var message = document.createElement("div");
  message.classList.add("bg-white", "rounded", "p-3", "mx-3", "shadow", "mb-3", "overflow-auto", "w-75", "mx-auto");

  // Создаем заголовок
  var header = document.createElement("p");
  header.classList.add("h4");
  header.innerText = data.title;
  message.appendChild(header);

  if (data.enable) {
    var explanation = document.createElement("div");
    explanation.classList.add("alert", "alert-light", "font-monospace");
    explanation.innerHTML = data.explanation;
    message.appendChild(explanation);
  }

  // Добавляем содержимое сообщения
  var content = document.createElement("div");
  content.innerHTML = data.html;
  message.appendChild(content);

  var messageContainer = document.querySelector("#message-container");
  messageContainer.appendChild(message);

  window.scrollTo(0, document.body.scrollHeight);
}
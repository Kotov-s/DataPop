// $("#my-form").submit(function (e) {
//   e.preventDefault();

//   // Get the values of the selected options
//   var analysisOption = $("#analysis-options").val();
//   var columns = $("#columns").val();

//   // Generate the message
//   var message = "You selected analysis option " + analysisOption + " and columns " + columns.join(", ");

//   alert(message);
// });



$("#my-form").submit(function (e) {
  e.preventDefault();

  // Get the values of the selected options
  var analysisOption = $("#analysis-options").val();
  var columns = $("#columns").val();
  // Make the AJAX request
  $.ajax({
      type: "POST",
      url: `/chat/return_message/${userId}/${csvSlug}`,
      data: {
          "analysisOption": analysisOption,
          "columns": columns,
          "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (data) {
          createMessage(data);
      },
      error: function (error) {
          alert("An error occurred: " + error);
      }
  });

  
});

function createMessage(data) {
  // Create a new div element
  var message = document.createElement("div");
  // Set the innerHTML of the div element to the data received from the AJAX request
  message.innerHTML = data;
  message.classList.add("bg-white", "rounded", "p-3", "mx-3", "shadow", "mb-3", "overflow-auto");
  var messageContainer = document.querySelector("#message-container");
  messageContainer.appendChild(message);
  window.scrollTo(0, document.body.scrollHeight);
}







// document.getElementById("chat-submit").addEventListener("click", function(event) {
//   event.preventDefault();
//   var formData = new FormData(document.getElementById("my-form"));
//   var xhr = new XMLHttpRequest();
//   xhr.open("POST", "/chat/return_message/");
//   xhr.onload = function() {
//     if (xhr.status === 200) {
//       // Handle successful response
//       var message = xhr.responseText;
//       // Display the message on the page
//       document.getElementById("chat-output").innerHTML = message;
//     } else {
//       // Handle error response
//     }
//   };
//   xhr.send(formData);
// });


// $(function () {
//   setTimeout(function() {      
//     generate_message('Это юмореска-бот. Введите слово по которому хотите найти анекдот', 'user');  
//   }, 0);
//   var INDEX = 0; 
//   $("#chat-submit").click(function (e) {
//     e.preventDefault();
//     var msg = $("#chat-input").val();
//     if (msg.trim() == '') {
//       return false;
//     }

//     var buttons = [
//       {
//         name: 'Existing User',
//         value: 'existing'
//       },
//       {
//         name: 'New User',
//         value: 'new'
//       }
//     ];
  

//     generate_message(msg, 'self');

//     $.ajax({
//       type: "GET",
//       url: '/chat/return_message',
//       data: {
//           "result": msg,
//       },
//       dataType: "json",
//       success: function (data) {

//         if(msg.trim() == ''){
//           return false;
//         }
        
//         var buttons = [
//             {
//               name: 'Existing User',
//               value: 'existing'
//             },
//             {
//               name: 'New User',
//               value: 'new'
//             }
//           ];
//         setTimeout(function() {      
//           generate_message(data['result'], 'user');  
//         }, 0)


//       },
//       failure: function () {
//           alert("failure");
//       }
//   });

//   })



//   function generate_message(msg, type) {
//     INDEX++;
//     let str = "";
//     let avatar = type === 'self' ? userAvatar : botAvatar;
//     // let sectionClass = type === 'self' ? 'comment-section-user' : 'comment-section-bot';
//     str += `<div class='bg-white m-3 p-3 rounded shadow'>`;
//     str += `<div class='message-header-container'>`;
//     str += `<img style="width: 32px; height: 32px;" class="rounded-5" src="${avatar}">`;    
//     str += `<span class='message-line'>sdfsdfsdf</span>`;
//     str += `</div>`;
//     str += `<div class='message-content'>`;
//     str += `<div class="message-header">${msg}</div></div></div>`;
//     $(".chat-logs").append(str);
//     $("#cm-msg-" + INDEX).hide().fadeIn(0);
//     if (type === 'self') {
//         $("#chat-input").val('');
//     }
//     $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
// }


//   // function generate_button_message(msg, buttons) {
//   //   /* Buttons should be object array 
//   //     [
//   //       {
//   //         name: 'Existing User',
//   //         value: 'existing'
//   //       },
//   //       {
//   //         name: 'New User',
//   //         value: 'new'
//   //       }
//   //     ]
//   //   */
//   //   INDEX++;
//   //   var btn_obj = buttons.map(function (button) {
//   //     return "              <li class=\"button\"><a href=\"javascript:;\" class=\"btn btn-primary chat-btn\" chat-value=\"" + button.value + "\">" + button.name + "<\/a><\/li>";
//   //   }).join('');
//   //   var str = "";
//   //   str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg user\">";
//   //   str += "          <span class=\"msg-avatar\">";
//   //   str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
//   //   str += "          <\/span>";
//   //   str += "          <div class=\"cm-msg-text\">";
//   //   str += msg;
//   //   str += "          <\/div>";
//   //   str += "          <div class=\"cm-msg-button\">";
//   //   str += "            <ul>";
//   //   str += btn_obj;
//   //   str += "            <\/ul>";
//   //   str += "          <\/div>";
//   //   str += "        <\/div>";
//   //   $(".chat-logs").append(str);
//   //   $("#cm-msg-" + INDEX).hide().fadeIn(300);
//   //   $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
//   //   $("#chat-input").attr("disabled", true);
//   // }

//   // $(document).delegate(".chat-btn", "click", function() {
//   //   var value = $(this).attr("chat-value");
//   //   var name = $(this).html();
//   //   $("#chat-input").attr("disabled", false);
//   //   generate_message(name, 'self');
//   // })

//   // $("#chat-circle").click(function() {    
//   //   $("#chat-circle").toggle('scale');
//   //   $(".chat-box").toggle('scale');
//   // })

//   // $(".chat-box-toggle").click(function() {
//   //   $("#chat-circle").toggle('scale');
//   //   $(".chat-box").toggle('scale');
//   // })

// })
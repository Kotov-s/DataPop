$(function () {
  setTimeout(function() {      
    generate_message('Это юмореска-бот. Введите слово по которому хотите найти анекдот', 'user');  
  }, 0);
  var INDEX = 0; 
  $("#chat-submit").click(function (e) {
    e.preventDefault();
    var msg = $("#chat-input").val();
    if (msg.trim() == '') {
      return false;
    }

    var buttons = [
      {
        name: 'Existing User',
        value: 'existing'
      },
      {
        name: 'New User',
        value: 'new'
      }
    ];
  

    generate_message(msg, 'self');

    $.ajax({
      type: "GET",
      url: '/chat/return_message',
      data: {
          "result": msg,
      },
      dataType: "json",
      success: function (data) {

        if(msg.trim() == ''){
          return false;
        }
        
        var buttons = [
            {
              name: 'Existing User',
              value: 'existing'
            },
            {
              name: 'New User',
              value: 'new'
            }
          ];
        setTimeout(function() {      
          generate_message(data['result'], 'user');  
        }, 0)


      },
      failure: function () {
          alert("failure");
      }
  });

  })



  function generate_message(msg, type) {
    INDEX++;
    let str = "";
    let avatar = type === 'self' ? userAvatar : botAvatar;
    let sectionClass = type === 'self' ? 'comment-section-user' : 'comment-section-bot';
    str += `<div class='${sectionClass} message-box'>`;
    str += `<div class='message-header-container'>`;
    str += `<img class='profile-img' src="${avatar}">`;    
    str += `<span class='message-line'>sdfsdfsdf</span>`;
    str += `</div>`;
    str += `<div class='message-content'>`;
    str += `<div class="message-header">${msg}</div></div></div>`;
    $(".chat-logs").append(str);
    $("#cm-msg-" + INDEX).hide().fadeIn(0);
    if (type === 'self') {
        $("#chat-input").val('');
    }
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
}


  // function generate_button_message(msg, buttons) {
  //   /* Buttons should be object array 
  //     [
  //       {
  //         name: 'Existing User',
  //         value: 'existing'
  //       },
  //       {
  //         name: 'New User',
  //         value: 'new'
  //       }
  //     ]
  //   */
  //   INDEX++;
  //   var btn_obj = buttons.map(function (button) {
  //     return "              <li class=\"button\"><a href=\"javascript:;\" class=\"btn btn-primary chat-btn\" chat-value=\"" + button.value + "\">" + button.name + "<\/a><\/li>";
  //   }).join('');
  //   var str = "";
  //   str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg user\">";
  //   str += "          <span class=\"msg-avatar\">";
  //   str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
  //   str += "          <\/span>";
  //   str += "          <div class=\"cm-msg-text\">";
  //   str += msg;
  //   str += "          <\/div>";
  //   str += "          <div class=\"cm-msg-button\">";
  //   str += "            <ul>";
  //   str += btn_obj;
  //   str += "            <\/ul>";
  //   str += "          <\/div>";
  //   str += "        <\/div>";
  //   $(".chat-logs").append(str);
  //   $("#cm-msg-" + INDEX).hide().fadeIn(300);
  //   $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
  //   $("#chat-input").attr("disabled", true);
  // }

  // $(document).delegate(".chat-btn", "click", function() {
  //   var value = $(this).attr("chat-value");
  //   var name = $(this).html();
  //   $("#chat-input").attr("disabled", false);
  //   generate_message(name, 'self');
  // })

  // $("#chat-circle").click(function() {    
  //   $("#chat-circle").toggle('scale');
  //   $(".chat-box").toggle('scale');
  // })

  // $(".chat-box-toggle").click(function() {
  //   $("#chat-circle").toggle('scale');
  //   $(".chat-box").toggle('scale');
  // })

})
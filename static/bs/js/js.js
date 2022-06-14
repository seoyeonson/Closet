// chatbot
$(function(){

  $("#chatbot").click(function(){
    $("#chatbot").hide(600);
    $("#chatbot_chat").show(600);
  }); 
  
  $("#close").click(function(){
    $("#chatbot").show(500);
    $("#chatbot_chat").hide(500);
  }); 
  
  // $("#chatbot").click(function(){
  //   $("#chatbot_chat").css('display', 'block');
  //   show_intro_msg();
  // }); 

  // $("#close").click(function(){
  //   $("#chatbot_chat").css('display', 'none');
  // }); 
  
  // SEND 버튼을 누르거나
  $("#sendbtn").click(function(){
      send_message();
  }); 

  // ENTER key 가 눌리면
  $("#chattext").keyup(function(event){
      if(event.keyCode == 13){
          send_message()
      }
  })

})

function showClock(){
  var currentDate = new Date();
  var divClock = document.getElementById('divClock');
  var msg = "";
  if(currentDate.getHours()>12){      //시간이 12보다 크다면 오후 아니면 오전
      msg += "오후 ";
      msg += currentDate.getHours()-12+":";
  }
  else {
  msg += "오전 ";
  msg += currentDate.getHours()+":";
  }

  msg += currentDate.getMinutes()+"분 ";

  divClock.innerText = msg;
}

function send_message(){
  const chattext = $("#chattext").val().trim();

  // 입력한 메세지가 없으면 리턴
  if(chattext == ""){
      $("#chattext").focus();
      return;
  }

  // 입력한 채팅 화면에 출력
  const addtext = "<div class='mytext'> <span class='mytext_span'>" + chattext + "</span></div>";
  $("#chatbox").append(addtext);

  // 먼저 입력했던 것은 지우기
  $("#chattext").val("");
  $("#chattext").focus();

  // API 서버에 요청할 데이터
  
  const jsonData = {
      query: chattext
  }

  $.ajax({
      url: 'http://127.0.0.10:5000/query/TEST',
      type: "POST",
      data: JSON.stringify(jsonData),
      dataType: "JSON",   // 응답받을 데이터 타입
      contentType: "application/json; charset=utf-8",

      success: function(response){
          // 답변텍스트는 response.Answer 에 담겨 있다

          $chatbox = $("#chatbox");

          let bottext = '';

          if(response.Product_info){
            if(!(response.Product_info.hasOwnProperty('notice')))
            bottext +=  `<img src="/media/${response.Product_info['product_image']}" class='botimg'></img>`;
          }

          // 답변출력
          bottext += `<div><div class='bottext_div'>${response.Answer}`;

          
          if (response.Product_info) {
            if(response.Product_info.hasOwnProperty('notice')){
              const options = `<br><br><span>[사이즈]</span> ${response.Product_info['sizes']}<br><span>[색상]</span> ${response.Product_info['colors']}<br><br>`
              bottext += options
            } else {
              const bot_info = `<br><br><span>[상품명]</span> ${response.Product_info['product_name']}<br><span>[상품가격]</span> ${response.Product_info['product_price']}<br><br> <a href="http://127.0.0.1:8000/product/${response.Product_info['product_name']}" target='_blank' class='go_product' >상품 보러가기</a>`;
              bottext += bot_info;
            }
          };


          bottext += "</div></div>"
          $chatbox.append(bottext).fadeIn(300);

          // 스크롤 조정하기
          $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')});
      }
  });




}
function count(type)  {
  // 결과를 표시할 element
  const resultElement = document.getElementById('result');
  
  // 현재 화면에 표시된 값
  let number = resultElement.innerText;
  
  // 더하기/빼기
  if(type === 'plus') {
    number = parseInt(number) + 1;
  }else if(type === 'minus')  {
    number = parseInt(number) - 1;
  }
  
  // 결과 출력
  resultElement.innerText = number;
}

// chatbot
$(function(){
  
  $("#chatbot").click(function(){
    $("#chatbot_chat").css('display', 'block')
  }); 

  $("#close").click(function(){
    $("#chatbot_chat").css('display', 'none')
  }); 
  
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

function send_message(){
  const chattext = $("#chattext").val().trim();

  // 입력한 메세지가 없으면 리턴
  if(chattext == ""){
      $("#chattext").focus();
      return;
  }

  // 입력한 채팅 화면에 출력
  const addtext = "<div style='margin:15px 0;text-align:right;max-width:100vmin;'> <span style='padding:3px 10px;background-color:black;border-radius:3px;color:white;max-width:100vmin;'>" + chattext + "</span></div>";
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

          // 답변출력
          let bottext = "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#DDD;border-radius:3px;'>" + response.Answer + "</span></div>";
          if(response.Product_info){
            // const bot_info = $`<img src="/media/{0}">\n상품명:{1}\n상품가격:{2}`.format(
            //   response.Product_info['product_image'],
            //   response.Product_info['product_name'],
            //   response.Product_info['product_price']
            // )

            const bot_info = `<img src="/media/${response.Product_info['product_image']}">\n상품명:${response.Product_info['product_name']}\n상품가격:${response.Product_info['product_price']}`
            bottext +=  "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#DDD;border-radius:3px;'>"+ bot_info + "</span></div>" 
          }
          $chatbox.append(bottext);

          // 스크롤 조정하기
          $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')})  
      }
  });




}
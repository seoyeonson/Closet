// chatbot
$(function(){
  $(document ).on("click", "#plus_btn", function(){
    num = parseInt($('.p_cnt_input').val().trim())
    $('.p_cnt_input').val(num + 1)
  });  
  $(document ).on("click", "#minus_btn", function(){
    num = parseInt($('.p_cnt_input').val().trim())
    if(num > 1){
      $('.p_cnt_input').val(num - 1)
    };
  }); 
           

  $("#chatbot").click(function(){
    $("#chatbot").hide(600);
    $("#chatbot_chat").show(600);
  }); 
  
  $("#close").click(function(){
    $("#chatbot").show(500);
    $("#chatbot_chat").hide(500);
  }); 
  
  // SEND 버튼을 누르거나
  $("#sendbtn").click(function(){
      send_message();
      // 스크롤 조정하기
      $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')});
  }); 

  // ENTER key 가 눌리면
  $("#chattext").keyup(function(event){
      if(event.keyCode == 13){
          send_message()
          // 스크롤 조정하기
          $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')});
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
  const addtext = "<div class='mytext'> <span class='mytext_span'>" + chattext + "</span></div>";
  $("#chatbox").append(addtext);

  // 먼저 입력했던 것은 지우기
  $("#chattext").val("");
  $("#chattext").focus();

  // API 서버에 요청할 데이터
  
  const jsonData = {
      query: chattext
  }

  new Promise(function(resolve, reject){
    $chatbox = $("#chatbox");
    let bottext = '<div><div id="loading" class="bottext_div"><div class="spinner"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div></div></div>';
    $chatbox.append(bottext);
    resolve();
  }).then(function(result){
    $.ajax({
          url: 'http://127.0.0.10:5000/query/TEST',
          type: "POST",
          data: JSON.stringify(jsonData),
          dataType: "JSON",   // 응답받을 데이터 타입
          contentType: "application/json; charset=utf-8",
    
          success: function(response){
              // 답변텍스트는 response.Answer 에 담겨 있다

              $loading = $("#loading")
    
              let bottext = '';
    
              if(response.Product_info){
                if(!(response.Product_info.hasOwnProperty('notice')))
                bottext +=  `<img src="/media/${response.Product_info['product_image']}" class='botimg'></img>`;
              }
    
              // 답변출력
              bottext += `<div><div class='bottext_div'>${response.Answer}`;
    
              
              if (response.Product_info) {
                if(response.Product_info.hasOwnProperty('notice')){
                 sizes = response.Product_info['sizes']
                 colors = response.Product_info['colors']
                
                 localStorage.setItem('sizes', sizes)
                 localStorage.setItem('colors', colors)


                 bottext += "<br><br>"
                 bottext += order_select(sizes, colors)

                } else {
                  const bot_info = `<span>[상품명]</span> ${response.Product_info['product_name']}<br><span>[상품가격]</span> ${response.Product_info['product_price']}<br><br> <a href="http://127.0.0.1:8000/product/${response.Product_info['product_name']}" target='_blank' class='go_product' >상품 보러가기</a>`;
                  bottext += '<br><br>'
                  bottext += bot_info;
                };
              };
              bottext += '</div></div>'
              $loading.html(bottext);
              $loading.attr('class', '');
              $loading.attr('id', 'new');
    
              // 스크롤 조정하기
              $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')});
          }
      });
  })
}

function order_select(sizes, colors){
  sizes_list = ''
  colors_list = ''

  if (sizes){
    sizes = sizes.toString().split(',');
    console.log(typeof(sizes))
    for (var size of sizes){
    sizes_list += `<label class="test"><input type="radio" name="size" value="${size}"><span>${size}</span></label><br>`
  }
  } else if (colors){
    colors = colors.toString().split(',');
    console.log(typeof(colors))
      for (var color of colors){
    colors_list += `<label class="test" ><input type="radio" name="color" value="${color}"><span>${color}</span></label><br>`
  }
  }

  if(sizes_list != ''){
    sizes_list = '<p class="choice_title">[사이즈 선택]</p>' + sizes_list
  } else if (colors_list != ''){
    colors_list = '<p class="choice_title">[색상 선택]</p>' + sizes_list
  }

  options = `${sizes_list}${colors_list}`
  p_count = `<br><p class="choice_title">[수량 선택]</p><div><button class="p_cnt_btn" id="minus_btn"><i class="fa fa-minus p_minus" aria-hidden=true></i></button><input class="p_cnt_input" min="1" value=1 readonly><button class="p_cnt_btn" id="plus_btn"><i class="fa fa-plus p_plus" aria-hidden=true></i></button></div>`
  result = options + p_count + '<br><button class="info_submit"><span>구매하기</span></button>'

  return result
}; 
function buy(){
    var size = $('#size').val().trim()
    var color = $('#color').val().trim()

    if(size==""){
        alert("사이즈를 선택해주세요.")
        return false;
    }else if($('#color').val().trim()==""){
        alert("색상을 선택해주세요.")
        return false;
    }
    $('#product_buy').submit();
    return true;
};
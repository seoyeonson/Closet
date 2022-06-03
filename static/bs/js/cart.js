$(document).ready(function(){
    $("#all_agree").change(all_agree);
    $(".choice").change(del_agree);
    $("#auth_btn").click(phone_confirm);
    $("#confirm_btn").off().on("click",confirm_num);
    $("#purchase_btn").off().on("click",purchase);
    $(".plus-minus-btn").off().on("click", choice_people);

    // $("#peopleNum").change(change_peopleNum);
});

function all_agree(){
    if($("#all_agree").is(":checked")){
        $(".choice").prop("checked", true)        
    }else{
        $(".choice").prop("checked", false)        
    }
}

function del_agree(){
    var check = $(this).is(":checked")
    if(!check){
        $("#all_agree").prop("checked", false)
    };
};
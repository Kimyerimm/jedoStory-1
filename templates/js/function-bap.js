


$(document).ready(function() {
    $('#navbarToggleBtn').click(function() {
      $('#navbarNav').toggleClass('show');
    });

    $("#date-picker-button").click( function() {
        $("#date").toggle()   
    });
   
  
  });

$(document).ready(function() {
    $("#CommingSoon").click( function(){

        alert(" CommingSoon !")
    })
})
function selectDate(t){
    var day=$(t).val()
    if ( day=="" ) {
        return 
    }
    window.location.href = `/meal/lunch/${day}`;

    // $.ajax({
    //     type: 'post',
    //     url: `/meal/lunch/${day}`
    // })
    // .done(function (reponse) {
    //     alert(reponse)
    // })
             
}
$("#meal-englsih-korean").click( function(){
  
    $("#meal-englsih-korean").append(`<div id='waiting'> <img id="ai-image-loading-spin" src="/images/spin1.svg" ></div>`)
    var prompt=$("#meal-englsih").text()
    if ( prompt==""  ) { return }
    $.ajax({
        type: "POST",
        url: "/api/EnglsihToKorean",  // Replace with your server API endpoint
        data: {
            prompt:prompt,

        },
        success: function(response) {
            console.log( response.result )
            
            $("#ai-image-loading-spin").remove()
            $(".meal-englsih").removeClass("d-none")
            $("#meal-englsih-korean-text").text(response.result);
            $(".변역").hide(500)
            $("#waiting").remove()
        },
    })

})

function createImage(text){
            
            
            meal_text=""
            $(".meal-menu-item").each(function() {
                var t=$(this).text().replace(/\([^)]*\)/g, '')
                    t=t.replace(/[^가-힣]/g, '').trim();
                meal_text = meal_text + t  + ", "
            });
          
            meal_text =meal_text.slice(0, -2);
            console.log( meal_text)
            if ( meal_text=="") {
                alert(  "식단이 없습니다.")    
                retrun }
            
            // $(".meal-image").css("background-color", "white");
            $("#meal-image-btn").append(`
                        <img id="ai-image-loading-spin" src="/images/spin1.svg" >
            `)
            $(".meal-englsih").addClass("d-none")
            $("#meal-englsih-korean-text").text("")
            $("#ai").hide(500)
                // Make an AJAX call to your server to process GPT-3 and DALL-E
                //$("#result").hide()  
                $.ajax({
                    type: "POST",
                    url: "/api/generate",  // Replace with your server API endpoint
                    data: {
                        actionCode:"meal-text",
                        period:$("#period").text(),
                        prompt: meal_text,

                    },
                    success: function(response) {

                        $("#ai-image-loading-spin").remove()
                        $("#meal-englsih").text(response.result);
                        // $(".변역").show(500)
                        // $(".meal-englsih").show(500)
                        var prompt=response.result
                        
                        var size = "512x512";

                        $("#meal-image-btn").append(`
                        <img id="ai-image-loading-spin" src="/images/spin2.svg" >
                         `)
           
                        $.ajax({
                            type: "POST",
                            url: "/api/generate-image",  // Replace with your server API endpoint
                            data: {
                                actionCode:"create-image",
                                prompt: prompt,
                                size: size
                            },
                            success: function(response) {

                                console.log(  response)
                                id=response["dalle"]["created"]
                                $.each(response["dalle"]["data"], function(index, item) {

                                   $("#meal-image").prepend(`
                                        <img id="meal-image-${id}-${index}" class="p-1" src="${item["url"]}">
                                   `) 
                                })
                                $("#ai-image-loading-spin").remove()
                                $("#ai").show(500)
                            },
                            error: function() {
                                $("#ai-image-loading-spin").remove()
                                $("#result").text("An error occurred.");
                                $("#ai").show(500)
                            }
                        });
                    },
                    error: function() {
                        $("#result").text("An error occurred.");
                    }
                });
                return 
}
 
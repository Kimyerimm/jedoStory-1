$(document).ready(function() {
        $(window).resize(function () {
            if ( $('#navbarToggleBtn').is(":visible") ){
                $('#navbarNav').addClass("mt-3 border-top");
                } else {
                $('#navbarNav').removeClass("mt-3 border-top");
                }
        });

        if ( color_Theme()=="dark"){
            $("#menu").removeClass("bg-warning")
        } else {
            $("#menu").addClass("bg-warning")
        }
})

$('#navbarToggleBtn').click(function() {
    $('#navbarNav').toggleClass('show');
});

$(".dropdown-item").click(function() {
    var code=color_Theme(this)
    if ( code=="dark"){
            $("#menu").removeClass("bg-warning")
        } else {
        $("#menu").addClass("bg-warning")
        }
 });



function color_Theme(_this) {
    var colorMode="light"
    if ( _this ){
        colorMode=$(_this).attr("data-bs-theme-value") 
    } else {
        colorMode=$("#bd-theme").attr("aria-label")    
            try {
            colorMode= colorMode.indexOf("dark") ==-1 ? 'light':'dark'  
            } catch (error) {
            colorMode='light'
            }       
    }

    return  colorMode
}
function send_query() {

        var query = $("#query").val();
        if (query.trim() === "") return;
        $("#chat").append(`
                <div class='user_query p-2 fs-5'>
                        <i class="fa-thin fa-user fs-4"></i> ${query}
                </div>`);

        $("#query").val("");

        $.ajax({
            url: "/query",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: query }),
            success: function (response) {
                ans = response.answer;
                ans=ans.replace(/\n/g, "<br>");
                $("#chat").append(`
                    <div class='ai_answer p-2 fs-5'>
                        <i class="fa-solid fa-user-astronaut fs-4"></i> ${ans}
                    </div>
                `);

                // 스크롤 위치를 가장 하단으로 이동
                $("#chat").scrollTop(chatDiv[0].scrollHeight);
            },
            error: function () {
                $("#chat").append(`
                    <div class='ai_answer p-2 fs-5'>
                        <i class="fa-solid fa-user-astronaut fs-4 "></i> Server Error!
                    </div>
                `);
                $("#chat").scrollTop(chatDiv[0].scrollHeight);
            }
        });

        // 사용자가 메시지를 보낼 때도 스크롤 위치를 조정
        $("#chat").scrollTop(chatDiv[0].scrollHeight);
}
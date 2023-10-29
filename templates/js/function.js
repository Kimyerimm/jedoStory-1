$(document).ready(function() {
    $(window).resize(function () {
        if ( $('#navbarToggleBtn').is(":visible") ){
            $('#navbarNav').addClass("mt-3 border-top");
         } else {
           $('#navbarNav').removeClass("mt-3 border-top");
         }
    });

    if ( color_Theme()=="dark"){
        $("#top-menu").removeClass("bg-warning")
    } else {
       $("#top-menu").addClass("bg-warning")
    }
})

    $('#navbarToggleBtn').click(function() {
        $('#navbarNav').toggleClass('show');
    });

    $(".dropdown-item").click(function() {
        var code=color_Theme(this)
        if ( code=="dark"){
             $("#top-menu").removeClass("bg-warning")
         } else {
            $("#top-menu").addClass("bg-warning")
         }
      });
  


    function color_Theme(_this) {
        if ( _this ){
            var colorMode=$(_this).attr("data-bs-theme-value") 
        } else {
            var colorMode=$("#bd-theme").attr("aria-label")    
                colorMode= colorMode.indexOf("dark") ==-1 ? 'light':'dark'  
        }
        
        if ( colorMode=="light"){ return "light"}
        if ( colorMode=="dark"){  return "dark" }
        return  "light"
    }
    function send_query() {

        var colorMode=color_Theme()

        var query = $("#query").val();
        if (query.trim() === "") return;

        $("#chat").append(`
                <div class='${ colorMode=='dark' ? "text-secondary":"text-secondary"}'>
                   User: ${query}
                </div>
                `);
        $("#query").val("");

        $.ajax({
            url: "/query",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: query }),
            success: function (response) {

               ans=response.answer
            //    if ( query.indexOf("일정") !=-1){
            //         ans=ans.replaceAll(":-","<br>")
            //         ans=ans.replaceAll("-","<br>-") 
            //    }
               
                $("#chat").append(`
                    <div class='${ colorMode=='dark' ? "text-warning":"text-dark"}'>
                       <pre>제돌: ${ans}</pre>
                    </div>
                `);
            },
            error: function () {
                alert("Error sending query");
            }
        });
    }
    // function replaceAll(str, search, replacement) {
    //     return str.replace(new RegExp(escapeRegExp(search), 'g'), replacement);
    //   }    
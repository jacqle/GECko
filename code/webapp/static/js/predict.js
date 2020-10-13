$("#arrow-button").click(function(){
    var text = $("#textarea-input").text();
    
    $.ajax({
        url: "/predict",
        type: "get",
        data: {jsdata: text},
        success: function(response) {
            $("#textarea-output").html(response);
        },
        error: function(xhr) {
            //Do Something to handle error 
        }
    });
});
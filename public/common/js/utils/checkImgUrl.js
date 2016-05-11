var contacts = contacts || {}

contacts.utils.checkImgUrl = function(ficha){
    var url = "/fotos/F00" + ficha + ".jpg"
    var checkImgUrl = $.ajax({
        type: "GET",
        url: url,
    })

    checkImgUrl.done( function(data, statusText, xhr){
        $(".img"+ficha).attr("src", "/fotos/F00" + ficha + ".jpg")
    })

    checkImgUrl.fail( function(data, statusText, xhr){
         $(".img"+ficha).attr("src", "public/common/img/default.jpg")
    })
}


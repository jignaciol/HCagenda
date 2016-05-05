var contacts = contacts || {}

/*
contacts.utils.checkImgUrl = function(ficha){
    var url = "fotos/F00" + ficha + ".jpg"
    var req = new XMLHttpRequest();
    req.open("GET", url, false);
    req.send();
    if(req.status == 200){
        console.log("url encontrada")
        return url;
    } else {
        console.log("url no encontrada")
        return "public/common/img/default.jpg";
    }
};
*/

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


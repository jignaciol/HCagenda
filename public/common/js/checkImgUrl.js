var contacts = contacts || {}

contacts.utils.checkImgUrl = function(ficha){
    var url = "fotos/F00" + ficha + ".jpg"
    var req = new XMLHttpRequest();
    req.open("GET", url, false);
    req.send();
    if(req.status == 200){
        return url;
    } else {
        return "public/common/img/default.jpg";
    }
};

/*
contacts.utils.checkImgUrl = function(imgURL){
    $.ajax({
        type: "GET",
        async: false,
        url: imgURL,
        success: function(imgURL){
            return imgURL
        },
        error: function(){
            return "public/common/img/default.jpg"
        }
    })
}
*/

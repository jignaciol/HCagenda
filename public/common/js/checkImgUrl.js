var contacts = contacts || {}

contacts.utils.checkImgUrl = function(url){
    var req = new XMLHttpRequest();
    req.open("GET", url, false);
    req.send();
    if(req.status == 200){
        return url;
    } else {
        return "public/common/img/default.jpg";
    }
};

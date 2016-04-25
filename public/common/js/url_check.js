
function CheckUrl(url, cb){
    jQuery.ajax({
        url: url,
        dataType: 'text',
        type: 'GET',
        complete: function(xhr){
            if(typeof cb === 'function')
                cb.apply(this, [xhr.status]);
        }
    });
}

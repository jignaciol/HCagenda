var contacts = contacts || {}

contacts.utils.loadHtmlTemplate = function(templateName){

    self=this
    $.ajax({
        async: false,
        url: "/api/template/" + templateName + ".html",
        type: "GET",
        datatype: "text",
        success: function(response){
            self.htmlDevuelto = response
            return self.htmlDevuelto
        },

        error: function(response){
            self.htmlDevuelto = response
        }
    })
    return self.htmlDevuelto

 }

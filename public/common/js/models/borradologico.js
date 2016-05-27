var contacts = contacts || {}

contacts.models.borradoLogico = Backbone.Model.extend({

    url: "/api/borradologico",

    defaults: {
        descripcion: ""
    }

})

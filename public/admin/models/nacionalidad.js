var contacts = contacts || {}

contacts.models.nacionalidad = Backbone.Model.extend({

    url: "/api/nacionalidad",

    defaults: {
        descripcion: "",
        bl: 0,
        codigo: ""
    }

})

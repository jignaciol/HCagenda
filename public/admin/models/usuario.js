var contacts = contacts || {}

contacts.models.usuario = Backbone.Model.extend({

    url: "api/usuario",

    defaults: {
        username: "",
        nombre: "",
        apellido: "",
        fec_ing: ""
        bl: 1
    }

})

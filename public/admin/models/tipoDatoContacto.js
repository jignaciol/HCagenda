var contacts = contacts || {}

contacts.models.tipoDatoContacto = Backbone.RelationalModel.extend({

    url: "/api/tipodatocontacto",

    defaults: {
        descripcion: "",
        fec_ing: "",
        bl: 1
    }

})

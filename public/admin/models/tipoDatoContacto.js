var contacts = contacts || {}

contacts.models.tipoDatoContacto = Backbone.Model.extend({

    url: "/api/tipodatocontacto",

    defaults: {
        descripcion: "",
        fec_ing: "",
        bl: 1
    }

})

var contacts = contacts || {}

contacts.models.departamento = Backbone.Model.extend({

    url: "/api/departamento",

    defaults: {
        descripcion: "",
        fec_ing: "",
        id_ubicacion: 0,
        ubicacion: "",
        id_piso: 0,
        piso: "",
        bl: 1,
        estado: "",
        alias: ""
    }

})

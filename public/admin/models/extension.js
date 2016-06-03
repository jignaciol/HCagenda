var contacts = contacts || {}


contacts.models.extension = Backbone.Model.extend({

    url: "/api/extension",

    defaults: {
        id_departamento: 0,
        departamento: "",
        numero: "",
        fec_ing: "",
        bl: 1,
        estado: "",
        csp: "",
        tipo: "",
        modelo: "",
        serial: "",
        mac_pos: "",
        grupo_captura: "",
        status: "",
        lim: "",
        fecha_inventario: ""
    }

})

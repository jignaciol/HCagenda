var contacts = contacts || {}


contacts.models.extensiones = Backbone.Model.extend({

    url: "/api/extensiones",

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
        mac-pos: "",
        grupo_captura: "",
        status: "",
        lim: "",
        fecha_inventario: ""
    }

})

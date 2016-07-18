var contacts = contacts || {}

contacts.models.datoContacto = Backbone.Model.extend({

    urlRoot: "/api/datocontacto",

    defaults: {
        descripcion: "",
        fecha_ing: "",
        id_empleado: 0,
        id_tipo_contacto: 0,
        tipocontacto: ""
    }

})

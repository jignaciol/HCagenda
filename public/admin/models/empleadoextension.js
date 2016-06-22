var contacts = contacts || {}

contacts.models.empleadoExtension = Backbone.Model.extend({

    urlRoot: "/api/empleadoextension",

    defaults: {
        id_empleado: 0,
        empleado: "",
        bl: 0,
        id_extension: 0,
        fec_asignacion: "",
        numero: "",
        estado: ""
    }
})

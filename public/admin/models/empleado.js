var contacts = contacts || {}

contacts.models.empleado = Backbone.Model.extend({

    urlRoot: "/api/empleado",

    defaults: {
        ficha: "",
        voe: "",
        cedula: "",
        nombre: "",
        apellido: "",
        indicador: "",
        fecha_nac: "",
        fecha_ing: "",
        id_departamento: 0
    }

})

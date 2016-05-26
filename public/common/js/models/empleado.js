var contacts = contacts || {};

contacts.models.empleado = Backbone.Model.extend({

    urlRoot: "/api/empleado",

    idAttribute: "id_empleado",

    defaults: {
        ficha: '',
        voe: '',
        cedula: '',
        nombre: '',
        apellido: '',
        indicador: '',
        fecha_nac: '',
        fecha_ing: ''
    }

});

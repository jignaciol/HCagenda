var contacts = contacts || {};

contacts.models.empleado = Backbone.RelationalModel.extend({

    urlRoot: 'empleado/',

    idAttribute: 'id_empleado',

    defaults: {
        ficha: '',
        voe: '',
        cedula: '',
        nombre: '',
        apellido: '',
        indicador: '',
        fecha_nac: '',
        fecha_ing: ''
    },

    relations: [{
        type: Backbone.HasOne,
        key: "id_departamento",
        relatedModel: contacts.models.departamento,
        reverseRelation: {
            key: "id",
            includeInJSON: "id"
        }
    }]

});

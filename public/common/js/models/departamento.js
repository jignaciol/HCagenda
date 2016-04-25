var contacts = contacts || {};

contacts.models.departamento = Backbone.RelationalModel.extend({

    urlRoot: 'departamento/',

    idAttribute: 'id_departamento',

    defaults: {
        descripcion: '',
        fec_ing: '',
        bl: 1
    },

    relations: [{
        type: Backbone.HasOne,
        key: "id_ubicacion",
        relatedModel: contacts.models.area,
        reverseRelation: {
            key: "id",
            includeInJSON: "id"
            }
        },
        {
        type: Backbone.HasOne,
        key: "id_piso",
        relatedModel: contacts.models.area,
        reverseRelation: {
            key: "id",
            includeInJSON: "id"
        }
    }]

});

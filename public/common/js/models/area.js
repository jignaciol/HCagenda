var contacts = contacts || {};

contacts.models.area = Backbone.RelationalModel.extend({

    urlRoot: 'area/',

    idAttribute: 'id',

    defaults: {
        descripcion: '',
        fec_ing: '',
        bl: 1
    },

    relations: [{
        type: Backbone.HasOne,
        key: 'id_tipo_area',
        relatedModel: contacts.models.tipo_area,
        reverseRelation: {
            key: 'id_tipo_area',
            includeInJSON: 'id'
        }
    }]

});

var contacts = contacts || {};

contacts.models.tipoArea = Backbone.RelationalModel.extend({

    url: "/api/tipo_area",

    defaults: {
        'descripcion': null,
        'fec_ing': null,
        'bl': 1
    },

});

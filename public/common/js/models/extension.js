var contacts = contacts || {};

contacts.models.Extension = Backbone.RelationalModel.extend({

    urlRoot: "extension/",

    idAttribute: "id_extension",

    defaults: {
        descripcion: "",
        numero: ""
    },

});

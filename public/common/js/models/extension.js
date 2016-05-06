var contacts = contacts || {};

contacts.models.Extension = Backbone.RelationalModel.extend({

    urlRoot: "extensions/",

    defaults: {
        descripcion: "",
        numero: "",
        modelo: ""
    },

});

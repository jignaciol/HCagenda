var contacts = contacts || {};

contacts.models.Extension = Backbone.Model.extend({

    urlRoot: "extensions/",

    defaults: {
        descripcion: "",
        numero: "",
        modelo: ""
    },

});

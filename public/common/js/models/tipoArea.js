var contacts = contacts || {};

contacts.models.tipoArea = Backbone.RelationalModel.extend({

    urlRoot: "api/tipo_area/",

    idAttribute: "id",

    defaults: {
        descripcion: "",
        fec_ing: "",
        bl: 1
    }

});

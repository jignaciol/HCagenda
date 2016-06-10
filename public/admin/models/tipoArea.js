var contacts = contacts || {};

contacts.models.tipoArea = Backbone.Model.extend({

    urlRoot: "/api/tipo_area",

    defaults: {
        descripcion: "",
        fec_ing: "",
        bl: 1,
        estado: ""
    }

});

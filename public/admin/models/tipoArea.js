var contacts = contacts || {};

contacts.models.tipoArea = Backbone.Model.extend({

    url: "/api/tipo_area",

    defaults: {
        descripcion: "",
        fec_ing: "",
        bl: 1
    }

});

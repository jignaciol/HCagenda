var contacts = contacts || {};

contacts.models.departamento = Backbone.Model.extend({

    urlRoot: "/api/departamento",

    idAttribute: "id",

    defaults: {
        descripcion: '',
        fec_ing: '',
        bl: 1,
        id_ubicacion: 0,
        ubicacion: "",
        id_piso: 0,
        piso: ""
    }

});

var contacts = contacts || {}

contacts.models.area = Backbone.Model.extend({

    url: "/api/area",

    defaults: {
        descripcion: "",
        bl: 1,
        estado: "",
        id_tipo_area: 0,
        tipo_area: "",
        fec_ing: ""
    }

})

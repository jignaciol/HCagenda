var contacts = contacts || {}

contacts.models.menuOpcion = Backbone.Model.extend({

    url: "api/menuopcion",

    defaults: {
        descripcion: "",
        url: "",
        fec_asig: "",
        fec_desact : "",
        bl: 1
    }

})

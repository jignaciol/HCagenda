var contacts = contacts || {}

contacts.models.menuUsuario = Backbone.Model.extend({

    url: "api/menuusuario",

    defaults: {
        username: "",
        id_opcionMenu: 0,
        fec_asig: "",
        fec_desact: "",
        bl: 1
    }

})

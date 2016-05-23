var contacts = contacts || {}


contacts.collections.listaMenuUsario = Backbone.Collection.extend({

    url: "/api/menuusuario",

    model: contacts.models.menuUsuario
})

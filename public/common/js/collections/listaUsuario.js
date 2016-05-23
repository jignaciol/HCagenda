var contacts = contacts || {}

contacts.collections.listaUsuario = Backbone.Collection.extend({

    url: "/api/usuario",

    model: contacts.models.usuario

})

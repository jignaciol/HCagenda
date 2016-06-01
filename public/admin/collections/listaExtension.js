var contacts = contacts || {}

contacts.collections.listaExtension = Backbone.Collection.extend({

    url: "/api/extensiones",

    model: contacts.models.extensiones

})

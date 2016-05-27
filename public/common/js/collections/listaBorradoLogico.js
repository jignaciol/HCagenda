var contacts = contacts || {}

contacts.collections.listaBorradoLogico = Backbone.Collection.extend({

    url: "/api/borradologico",

    model: contacts.models.borradoLogico

})

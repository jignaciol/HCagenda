var contacts = contacts || {}

 contacts.collections.listaArea = Backbone.Collection.extend({

    url: "/api/area",

    model: contacts.models.area
})

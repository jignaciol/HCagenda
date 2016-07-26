var contacts = contacts || {}

contacts.collections.listaNacionalidad = Backbone.Collection.extend({

    url: "/api/nacionalidad",

    model: contacts.models.nacionalidad

})

var contacts = contacts || {}

contacts.collections.listaDepartamento = Backbone.Collection.extend({

    url: "/api/departamento",

    model: contacts.models.departamento

})

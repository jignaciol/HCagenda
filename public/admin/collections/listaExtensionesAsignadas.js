var contacts = contacts || {}

contacts.collections.listaExtensionesAsignadas = Backbone.Collection.extend({

    url: "/api/empleadoextension",

    model: contacts.models.empleadoExtension

})

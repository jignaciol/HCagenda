var contacts = contacts || {}

contacts.collections.listaDatosContacto = Backbone.Collection.extend({

    url: "/api/listadatocontacto",

    model: contacts.models.datosContacto
    
})

var contacts = contacts || {}

contacts.collections.listaTipoDatoContacto = Backbone.Collection.extend({

    url: '/api/tipodatocontacto',

    model: contacts.models.tipoDatoContacto

})

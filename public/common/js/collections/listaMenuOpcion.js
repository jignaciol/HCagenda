var contacts = contacts || {}

contacts.collections.listMenuOpcion = Backbone.Collection.extend({

    url: "/api/menuopcion",

    models: contacts.models.menuOpcion

})

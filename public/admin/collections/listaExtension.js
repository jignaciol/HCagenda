var contacts = contacts || {}

contacts.collections.extensionList = Backbone.Collection.extend({

    url: "/api/extension",

    model: contacts.models.extension

})

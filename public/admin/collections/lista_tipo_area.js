var contacts = contacts || {};

contacts.collections.lista_tipo_area = Backbone.Collection.extend({

    url: "/api/tipo_area",

    model: contacts.models.tipoArea

});

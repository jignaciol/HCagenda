var contacts = contacts || {};

contacts.collections.lista_tipo_area = Backbone.Collection.extend({

    url: 'tipo_area/',

    model: contacts.models.tipo_area

});

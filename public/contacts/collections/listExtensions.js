var contacts = contacts || {};

contacts.collections.listExtensions = Backbone.Collection.extend({

    url: "extensions/",

    model: contacts.models.Extension,

    searchByName: function(letters){
        if (letters == "") return this;

        var pattern = new RegExp(letters,"ig");

        return _(this.filter(function(extension){
            return pattern.test(extension.get("extension"));
        }));
    }
});

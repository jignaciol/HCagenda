var contacts = contacts || {}

contacts.views.ExtensionsView = Backbone.View.extend({

    tagName: "li",

    className: "contactItem",

    events: {

    },

    template: _.template( $("#tplExtensionItem").html() ),

    render: function() {
        this.$el.html(this.template())
        return this
    },

    initialize: function() {
        this.render()
    }

})

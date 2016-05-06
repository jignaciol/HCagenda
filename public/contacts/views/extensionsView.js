var contacts = contacts || {}

contacts.views.ExtensionsView = Backbone.View.extend({

    tagName: "li",

    className: "contactItem",

    events: {

    },

    template: _.template( $("#tplExtensionItem").html() ),

    render: function() {
        console.log(this.template)
        this.$el.html(this.template( this.model.toJSON() ))
        return this
    },

    initialize: function() {
        this.render()
    }

})

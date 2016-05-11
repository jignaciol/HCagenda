var contacts = contacts || {}

contacts.views.ExtensionsView = Backbone.View.extend({

    tagName: "li",

    className: "contactItem",

    events: {

    },

    template: _.template( contacts.utils.loadHtmlTemplate("ExtensionItem") ),

    render: function() {
        this.$el.html(this.template( this.model.toJSON() ))
        return this
    },

    initialize: function() {
        this.render()
    }

})

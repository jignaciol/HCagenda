var contacts = contacts || {}

contacts.views.extensionReg = Backbone.View.extend({

    tagName: "tr",

    className: "small",

    events: {
        "click .btn-edit": "edit",
        "click .btn-delete": "delete",
    },

    edit: function() {
        contacts.app.extensionUpdate = new contacts.views.extensionUpdate({ el: $("#formBody"), model: this.model })
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("extensionReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initialize: function() {
        this.render()
    }

})

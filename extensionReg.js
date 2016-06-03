var contacts = contacts || {}

contacts.views.extensionReg = Backbone.View.extend({

    tagName: "",

    className: "",

    events: {
        "click .btn-edit": "edit",
        "click .btn-delete": "delete",
        "click .btn-update": "update",
        "click .btn-cancel": "cancel"
    },

    edit: function() {

    },

    cancel: function() {
        this.render()
    },

    update: function() {

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

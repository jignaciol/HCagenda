var contacts = contacts || {}

contacts.views.empleadoReg = Backbone.View.extend({

    tagName: "tr",

    className: "small",

    events: {
        "click .btn-edit": "edit",
        "click .btn-delete": "delete"
    },

    edit: function() {
        contacts.app.formEmpleadoUpdate = new contacts.views.empleadoUpdate({ el: $("#formEmpleado"), collection: this.collection, model: this.model })
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("empleadoReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initiaize: function() {
        this.render()
    }

})

var contacts = contacts || {}

contacts.views.datoContactoReg = Backbone.View.extend({

    tagName: "tr",

    className: "small",

    events: {
        "click .btn-delete": "delete",
        "click .btn-edit-dc": "edit"
    },

    edit: function() {
        console.log("presionado boton editar datocontacto")
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("datosContactoReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initiaize: function() {
        this.render()
    }

})

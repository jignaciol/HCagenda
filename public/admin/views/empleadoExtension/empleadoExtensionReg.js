collection: var contacts = contacts || {}

contacts.views.empleadoExtensionReg = Backbone.View.extend({

    tagName: "tr",

    className: "small",

    events: {
        "click .btn-edit": "edit",
        "click .btn-delete": "delete",
        "click .btn-update": "update",
        "click .btn-cancel": "cancel"
    },

    edit: function() {
        console.log("editando")
        this.$('.btn-edit').hide()
        this.$('.btn-delete').hide()
        this.$('.btn-update').show()
        this.$('.btn-cancel').show()

        empleado = this.model.get("id_empleado")
        extension = this.model.get("id_extension")
        bl = this.model.get("bl")

        contacts.utils.loadSelectEmpleado(empleado, "enable", this.$(".empleado"))
        contacts.utils.loadSelectExtensiones(extension, "enable", this.$(".extension"))
        contacts.utils.loadSelectBL( bl , "enable", this.$(".estado"))

    },

    update: function() {
        self = this
        this.model.set({
            id_empleado: this.$(".select-empleado").val() ,
            empleado: this.$(".select-empleado option:selected").html(),
            id_extension: this.$(".select-extension").val(),
            numero: this.$(".select-extension option:selected").html(),
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html()
        })
        this.model.save({
            success: function() {
                self.render()
            }
        })

    },

    cancel: function() {
        this.render()
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("empleadoExtensionReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initialize: function() {
        this.render()
    }

})

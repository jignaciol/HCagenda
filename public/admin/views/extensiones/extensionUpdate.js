var contacts = contacts || {}

contacts.views.extensionUpdate = Backbone.View.extend({

    events: {
        "click .btn-cancel": "cancel",
        "click .btn-update": "update"
    },

    update: function() {
        console.log("actualizando")
        self = this
        this.model.set({
            id_departamento: this.$(".select-departamento").val()

        })
        this.model.save({
            success: function() {
                self.cancel()
            }
        })

    },

    cancel: function() {
        $("#updateExtensiones").modal("hide")
        $(".modal-backdrop").remove()
        contacts.app.extensionUpdate = null
        this.dispose()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("extensionesUpdate") ),

    render: function() {
        this.$el.html(this.template(this.model.toJSON()))
        departamento = this.model.get("id_departamento")
        bl = this.model.get("bl")
        contacts.utils.loadSelectDepartamento(departamento, "enable", this.$("#selectDepartamento"))
        contacts.utils.loadSelectBL(bl, "enable", this.$("#selectEstado"))
        this.$("#updateExtensiones").modal({backdrop: 'static'})
        return this
    },

    dispose: function() {
        this.undelegateEvents()
        this.off()
        this.$el.removeData().unbind()
    },

    initialize: function() {
        this.render()
    }

})

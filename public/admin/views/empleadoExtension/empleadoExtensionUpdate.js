var contacts = contacts || {}

contacts.views.extensionUpdate = Backbone.View.extend({

    events: {
        "click .btn-cancel": "cancel",
        "click .btn-update": "update"
    },

    update: function() {
        self = this
        this.model.set({
            id_departamento: this.$(".select-departamento").val(),
            numero: this.$("#numeroExt").val(),
            bl: this.$(".select-bl").val(),
            csp: this.$("#cspExt").val(),
            tipo: this.$("#tipoExt").val(),
            modelo: this.$("#modeloExt").val(),
            serial: this.$("#serialExt").val(),
            mac_pos: this.$("#macposExt").val(),
            grupo_captura: this.$("#grupoCaptura").val(),
            status: this.$("#statusExt").val(),
            lim: this.$("#limExt").val(),
            fecha_inventario: this.$("#fechaInv").val()
        })
        this.model.save().done(function(){
            self.cancel()
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

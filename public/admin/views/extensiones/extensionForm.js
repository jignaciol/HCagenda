var contacts = contacts || {}

contacts.views.extensionForm = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("extensionesForm") ),

    events: {
        "click .btn-save-extension": "addExtension"
    },

    addExtension: function() {
        console.log("agregando extension")
        self = this
        /*
        extension = new contacts.models.extension()
        extension.set({
            id_departamento: this.$(".select-departamento").val(),
            departamento: this.$(".select-departamento option:selected").html(),
            numero: this.$("#numeroExt").val(),
            fec_ing: new Date().toJSON().slice(0, 10),
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html(),
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

        extension.save().done(function(response){
            id = response["id"]
            extension.set({id: id})
            self.collection.add(extension)
            $("#fondoForm").modal("hide")
        })
       */
        $("#formExtensiones").modal("hide")
        $(".modal-backdrop").remove()
        contacts.app.formExtension = null
        this.dispose()
    },

    dispose: function() {
        // COMPLETELY UNBIND THE VIEW

        this.undelegateEvents()
        this.off()
        this.$el.removeData().unbind()

        // Remove view from DOM

        //this.remove()
        //Backbone.View.prototype.remove.call(this)
    },

    render: function() {
        this.$el.html(this.template())
        contacts.utils.loadSelectExtension(0, "enable", this.$("#selectDepartamento"))
        contacts.utils.loadSelectBL(0, "enable", this.$("#selectEstado"))
        this.$("#formExtensiones").modal({backdrop: 'static'})
        return this
    },

    initialize: function() {
        this.render()
    }

})

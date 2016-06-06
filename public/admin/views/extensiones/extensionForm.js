var contacts = contacts || {}

contacts.views.extensionForm = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("extensionesForm") ),

    events: {
        "click .btn-add": "addExtension"
    },

    addExtension: function() {
        self = this
        extension = new contacts.models.extension()
        extension.set({
            id_departamento: this.$("#depatamento").val(),
            departamento: this.$("#departamento option:selected").html(),
            numero: this.$("#numeroExt").val(),
            fec_ing: new Date().toJSON().slice(0, 10),
            bl: this.$("#estadoslct").val(),
            estado: this.$("#estadoslct option:selected").html(),
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
            $(".modal-backdrop").attr("fade out")
        })

        this.dispose()
    },

    dispose: function() {
        this.off()
    },

    render: function() {
        this.$el.html(this.template())
        return this
    },

    initialize: function() {
        this.render()
    }

})

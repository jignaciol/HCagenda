var contacts = contacts || {}

contacts.views.datoContactoReg = Backbone.View.extend({

    tagName: "tr",

    className: "small",

    template: _.template( contacts.utils.loadHtmlTemplate("datosContactoReg") ),

    events: {
        'click .btn-delete': 'delete',
        'click .btn-edit': 'edit',
        'click .btn-cancel': 'cancel',
        'click .btn-update': 'update'
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
        return false
    },

    edit: function() {
        this.$(".btn-edit").hide()
        this.$(".btn-delete").hide()
        this.$(".btn-update").show()
        this.$(".btn-cancel").show()

        var descripcion = this.$('.descripcion').html()

        objetivo = this.$(".tipocontacto")
        tipoDatoContacto = this.model.get("id_tipo_contacto")
        contacts.utils.loadSelectTipoDatoContacto(tipoDatoContacto, "enable", objetivo)

        this.$('.descripcion').html('<input type="text" class="form-control descripcion-update small" value="' + descripcion + '">')

        return false
    },

    update: function() {
        self = this
        this.model.set({
            descripcion: this.$(".descripcion-update").val(),
            id_tipo_contacto: this.$(".select-tipoDatoContacto").val(),
            tipocontacto: this.$(".select-tipoDatoContacto option:selected").html()
        })

        this.model.save({
            success: function() {
                self.render()
            }
        })
        return false
    },

    cancel: function() {
        this.render()
        return false
    },

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initiaize: function() {
        this.render()
    }

})

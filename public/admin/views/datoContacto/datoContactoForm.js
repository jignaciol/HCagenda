var contacts = contacts || {}

contacts.views.datoContactoForm = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("datosContactoForm") ),

    events: {
        "click .btn-addDatoContacto": "addDatoContacto"
    },

    addDatoContacto: function() {
        self = this
        datoContacto = new contacts.models.datoContacto()
        datoContacto.set({
            id_empleado: this.model.get("id"),
            descripcion: this.$("#descripcion").val(),
            fecha_ing: new Date().toJSON().slice(0, 10),
            id_tipo_contacto: this.$(".select-tipoDatoContacto").val(),
            tipocontacto: this.$(".select-tipoDatoContacto option:selected").html()
        })

        datoContacto.save().done(function(response){
            id = response["id"]
            datoContacto.set({id: id})
            self.collection.add(datoContacto)
        })

        console.log(datoContacto)
    },

    render: function() {
        this.$el.html(this.template())
        contacts.utils.loadSelectTipoDatoContacto(0, "enable", this.$(".tipoDatoContacto"))
        return this
    },

    initialize: function() {
        this.render()
    }

})

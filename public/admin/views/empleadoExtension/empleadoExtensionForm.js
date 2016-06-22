var contacts = contacts || {}

contacts.views.empleadoExtensionForm = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("empleadoExtensionForm") ),

    events: {
        "click .btn-asignar": "asignar",
    },

    dispose: function() {
        this.undelegateEvents()
        this.off()
        this.$el.removeData().unbind()
    },

    asignar: function() {
        self = this
        eextension = new contacts.models.empleadoExtension()
        eextension.set({
            id_empleado: this.$(".select-empleado").val(),
            empleado: this.$(".select-empleado option:selected").html(),
            bl: this.$(".select-bl").val(),
            id_extension: this.$(".select-extension").val(),
            fec_asignacion: new Date().toJSON().slice(0, 10),
            numero: this.$(".select-extension option:selected").html(),
            estado: this.$(".select-bl option:selected").html()
        })
        console.log(eextension)
        eextension.save().done(function(response){
            id = response["id"]
            eextension.set({id: id})
            self.collection.add(eextension)
        })

    },

    render: function() {
        this.$el.html(this.template())
        contacts.utils.loadSelectEmpleado(0, "enable", this.$(".empleado"))
        contacts.utils.loadSelectExtensiones(0, "enable", this.$(".extension"))
        contacts.utils.loadSelectBL(0, "enable", this.$(".estado"))
        return this
    },

    initialize: function() {
        this.render()
    }

})

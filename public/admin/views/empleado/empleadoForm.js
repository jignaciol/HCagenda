var contacts = contacts || {}

contacts.views.empleadoForm = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("empleadoForm") ),

    events: {
        "click .btn-save": "addEmpleado",
        "click .btn-cancel": "cancel",
        "click .btn-close": "close"
    },

    cancel: function() {
       this.$("#formEmpleado").modal("hide")
       $(".modal-backdrop").remove()
       this.dispose()
    },

    dispose: function() {
       this.undelegateEvents()
       this.off()
       this.$el.removeData().unbind()
    },

    close: function() {

    },

    addEmpleado: function() {
        self = this

        empleado = new contacts.models.empleado()
        empleado.set({
            ficha: this.$("#ficha").val(),
            voe: this.$("#nacionalidad").val(),
            cedula: this.$("#cedula").val(),
            nombre: this.$("#nombre").val(),
            apellido: this.$("#apellido").val(),
            indicador: this.$("#indicador").val(),
            fecha_nac: this.$("#fecha_nac").val(),
            fecha_ing: new Date().toJSON().slice(0, 10),
            id_departamento: this.$(".select-departamento").val(),
            bl: this.$(".select-bl").val()
        })

        empleado.save()
            .done(function(response){
                self.$(".btn-cancel").toggle("slow")
                self.$(".btn-save").toggle("slow")
                self.$(".btn-close").toggle("slow")

                contacts.app.datoContactoCrud = new contacts.views.datoContactoCrud({ el: self.$(".datosContacto"), model: empleado})

                id = response["id"]
                empleado.set({id: id})
                self.collection.add(empleado)
        })

        /*
        this.$("#formEmpleado").modal("hide")
        this.$(".modal-backdrop").remove()
        this.dispose()
       */
    },

    render: function() {
        this.$el.html(this.template())
        this.$("#formEmpleado").modal({backdrop: 'static'})
        contacts.utils.loadSelectBL(0, "enable", this.$("#estado"))
        contacts.utils.loadSelectDepartamento(0, "enable", this.$("#departamento"))
        this.$("#fecha_nac").datepicker({
            dateFormat: 'yy-mm-dd',
            autoSize: true,
            changeYear: true,
            yearRange: "1930:2010",
        })

        /* contacts.app.datoContactoCrud = new contacts.views.datoContactoCrud({ el: this.$(".datosContacto") }) */

        /*Vista de datos de contacto*/
        return this
    },

    initialize: function() {
        this.render()
    }

})

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
        this.$("#formEmpleado").modal("hide")
        this.$(".modal-backdrop").remove()
        this.dispose()
    },

    addEmpleado: function() {
        self = this
        this.model.set({
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

        this.model.save().done(function(response){
            self.$(".btn-cancel").toggle("slow")
            self.$(".btn-save").toggle("slow")
            self.$(".btn-close").toggle("slow")

            self.$('#ficha').prop('disabled', true)
            self.$('#nacionalidad').prop('disabled', true)
            self.$('#cedula').prop('disabled', true)
            self.$('#nombre').prop('disabled', true)
            self.$('#apellido').prop('disabled', true)
            self.$('#indicador').prop('disabled', true)
            self.$('#fecha_nac').prop('disabled', true)
            self.$('.select-departamento').prop('disabled', true)
            self.$('.select-bl').prop('disabled', true)

            id = response["id"]
            self.model.set({id: id})
            self.collection.add(self.model)
        })
    },

    render: function() {
        this.$el.html(this.template())
        this.$("#formEmpleado").modal({backdrop: 'static'})
        contacts.utils.loadSelectBL(0, "enable", this.$("#estado"))
        contacts.utils.loadSelectDepartamento(0, "enable", this.$("#departamento"))
        this.$("#fecha_nac").datepicker({
            dateFormat: "yy/mm/dd",
            dayNames: [ "Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado" ],
            dayNamesMin: [ "Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa" ],
            firstDay: 1,
            gotoCurrent: true,
            monthNames: [ "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Deciembre" ]
        })
        return this
    },

    addDatoContacto: function() {
        contacts.app.datoContactoCrud = new contacts.views.datoContactoCrud({
            el: this.$(".datosContacto"),
            model: this.model,
            collection: this.collection
        })
        contacts.app.datoContactoCrud.showData()
    },

    initialize: function() {
        this.collection.on('add', this.addDatoContacto, this)
        this.render()
    }

})

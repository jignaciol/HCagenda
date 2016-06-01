var contacts = contacts || {}

contacts.views.departamentoForm = Backbone.View.extend({

    events: {
        "click .btn-agrega-dpto": "addDepartamento"
    },

    addDepartamento: function() {
        self = this
        departamento = new contacts.models.departamento()
        departamento.set({
            descripcion: this.$(".input-desc-dpto").val(),
            id_ubicacion: this.$(".select-ubicacion_1").val(),
            ubicacion: this.$(".select-ubicacion_1 option:selected").html(),
            id_piso: this.$(".select-ubicacion_2").val(),
            piso: this.$(".select-ubicacion_2 option:selected").html(),
            fec_ing: new Date().toJSON().slice(0, 10),
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html(),
            alias: ""
        })

        this.$(".input-desc-dpto").val("")

        departamento.save().done(function(response){
            id = response['id']
            departamento.set({id: id })
            self.collection.add(departamento)
        })

    },

    template: _.template( contacts.utils.loadHtmlTemplate("departamentoForm") ),

    render: function() {
        this.$el.html( this.template() )
        this.cargaUbicacion()
        this.cargaPiso()
        this.cargaBL()
        return this
    },

    cargaUbicacion: function(){
        objetivo = this.$(".selectUbicacion")
        status = "enable"
        seleccionado = 0
        tipoArea = 1
        contacts.utils.loadSelectArea(seleccionado, status, objetivo, tipoArea)
    },

    cargaPiso: function(){
        objetivo = this.$(".selectPiso")
        status = "enable"
        seleccionado = 0
        tipoArea = 2
        contacts.utils.loadSelectArea(seleccionado, status, objetivo, tipoArea)
    },

    cargaBL: function(){
        objetivo = this.$(".selectEstado")
        status = "enable"
        seleccionado = 0
        contacts.utils.loadSelectBL(seleccionado, status, objetivo)
    },

    initialize: function() {
        this.render()
    }

})

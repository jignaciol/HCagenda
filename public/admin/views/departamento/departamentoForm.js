var contacts = contacts || {}

contacts.views.departamentoForm = Backbone.View.extend({

    events: {
        "click .btn-agrega-area": "addArea"
    },

    addArea: function() {
        self = this
        area = new contacts.models.area()
        area.set({
            descripcion: this.$(".input-desc-area").val(),
            id_tipo_area: this.$(".select-tipoArea").val(),
            tipo_area: this.$(".select-tipoArea option:selected").html(),
            fec_ing: new Date().toJSON().slice(0, 10),
            bl: this.$(".select-area-bl").val()
        })

        area.save().done(function(response){
            id = response['id']
            area.set({id: id })
            self.collection.add(area)
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

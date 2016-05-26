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
        return this
    },

    cargaUbicacion: function(){
        objetivo = this.$(".selectUbicacion")
        status = "enable"
        seleccionado = 0
        contacts.utils.loadSelectUbicacion(seleccionado, status, objetivo)
    },

    initialize: function() {
        this.render()
    }

})

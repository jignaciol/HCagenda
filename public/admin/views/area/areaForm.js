var contacts = contacts || {}

contacts.views.areaForm = Backbone.View.extend({

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
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html()
        })

        area.save().done(function(response){
            id = response['id']
            area.set({id: id })
            self.collection.add(area)
        })
    },

    template: _.template( contacts.utils.loadHtmlTemplate("areaForm") ),

    render: function() {
        this.$el.html( this.template() )
        this.cargaCombo()
        return this
    },

    cargaCombo: function(){
        objetivo = this.$(".selectTipoArea")
        status = "enable"
        seleccionado = 0
        contacts.utils.loadSelectTipoArea(seleccionado, status, objetivo)
        contacts.utils.loadSelectBL(0, "enable", this.$(".select-areaBl"))
    },

    initialize: function() {
        this.render()
    }

})

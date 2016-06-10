var contacts = contacts || {}

contacts.views.tipoDatoContactoForm = Backbone.View.extend({

    events: {
        'click .btn-agrega-tipoDatoC': 'addTipoDatoContacto'
    },

    addTipoDatoContacto: function() {
        self=this
        var descripcion = this.$(".input-desc-tipoDatoC").val()
        var bl = this.$(".select-bl").val()
        var estado = this.$(".select-bl option:selected").html()
        var fec_ing = new Date().toJSON().slice(0, 10)

        tipoDatoContacto = new contacts.models.tipoDatoContacto()
        tipoDatoContacto.set({
            descripcion: descripcion,
            fec_ing: fec_ing,
            bl: bl,
            estado: estado
        })

        tipoDatoContacto.save().done(function(response){
            id = response['id']
            tipoDatoContacto.set({id: id})
            self.collection.add(tipoDatoContacto)
        })
    },

    template: _.template( contacts.utils.loadHtmlTemplate("tipoDatoContactoForm") ),

    render: function() {
        this.$el.html( this.template() )
        contacts.utils.loadSelectBL(0, "enable", this.$(".select-tipoDC-bl"))
       return this
    },

    initialize: function() {
        this.render()
    }
})

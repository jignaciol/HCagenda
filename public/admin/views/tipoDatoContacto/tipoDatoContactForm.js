var contacts = contacts || {}

contacts.views.tipoDatoContactoForm = Backbone.View.extend({

    events: {
        'click .btn-agrega-tipoDatoC': 'addTipoDatoContacto'
    },

    addTipoDatoContacto: function() {
        self=this
        var descripcion = this.$(".input-desc-tipoDatoC").val()
        var bl = this.$(".select-tipoDatoC-bl").val()
        var fec_ing = new Date().toJSON().slice(0, 10)

        tipoDatoContacto = new contacts.models.tipoDatoContacto()
        tipoDatoContacto.set({'descripcion': descripcion})
        tipoDatoContacto.set({'fec_ing': fec_ing})
        tipoDatoContacto.set({'bl': bl})

        tipoDatoContacto.save().done(function(response){
            id = response['id']
            tipoDatoContacto.set({id: id})
            self.collection.add(tipoDatoContacto)
        })
    },

    template: _.template( contacts.utils.loadHtmlTemplate("tipoDatoContactoForm") ),

    render: function() {
        this.$el.html( this.template() )
       return this
    },

    initialize: function() {
        this.render()
    }
})

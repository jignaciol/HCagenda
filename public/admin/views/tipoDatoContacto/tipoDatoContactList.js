var contacts = contacts || {}

contacts.views.tipoDatoContactoList = Backbone.View.extend({

    renderTipoDatoContacto: function(tipoDatoContacto) {
        var tipoDatoContacto = new contacts.views.tipoDatoContactoReg({
            model: tipoDatoContacto
        })
        this.$el.append(tipoDatoContacto.render().el)
    },

    render: function() {
        this.$el.html('')
        self = this
        this.collection.forEach(function(tipoDatoContacto){
            self.renderTipoDatoContacto(tipoDatoContacto)
        })
    },

    ActualizarLista: function() {
        this.render()
    },

    reloadData: function() {
        self=this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    },

    initialize: function(){
        this.collection.on('add', this.render, this)
        this.collection.on('remove', this.render, this)
        this.collection.on('change', this.render, this)
        self = this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    }
})

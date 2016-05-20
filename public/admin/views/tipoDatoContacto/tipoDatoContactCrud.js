var contacts = contacts || {}

contacts.views.crudDatoContacto = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("CrudTipoDatoContacto") ),

    render: function() {
        this.$el.html( this.template() )
        this.collection = new contacts.collections.listaTipoDatoContacto()
        var tipoDatoContacto = new contacts.views.tipoDatoContactoForm({ el: this.$("#tipoDatoCForm"), collection: this.collection })
        var tipoDatoContactoList = new contacts.views.tipoDatoContactoList({ el: this.$("#tipoDatoCListBody"), collection: this.collection })
    },

    initialize: function() {
        this.render()
    },

    dispose: function() {
        this.off()
    }

})

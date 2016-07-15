var contacts = contacts || {}

contacts.views.datoContactoCrud = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("datosContactoCrud") ),

    render: function() {
        this.$el.html(this.template())
        this.collection = new contacts.collections.listaDatoContacto()
        contacts.app.datoContactoForm = new contacts.views.datoContactoForm({ el: this.$(".formBody"), collection: this.collection })
        contacts.app.datoContactoList = new contacts.views.datoContactoList({ el: this.$("#listBody"), collection: this.collection })
        console.log(this.model)
        return this
    },

    initialize: function() {
        this.render()
    }

})

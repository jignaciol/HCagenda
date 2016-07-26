var contacts = contacts || {}

contacts.views.datoContactoCrud = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("datosContactoCrud") ),

    render: function() {
        self=this
        this.$el.html(this.template())
        return this
    },

    showData: function() {
        listaDatoContacto = new contacts.collections.listaDatoContacto()

        contacts.app.datoContactoForm = new contacts.views.datoContactoForm({
                        el: this.$(".formBody"),
                        collection: listaDatoContacto,
                        model: this.model
        })

        contacts.app.datoContactoList = new contacts.views.datoContactoList({
                        el: this.$("#listBody"),
                        collection: listaDatoContacto
        })
    },

    initialize: function() {
        this.render()
    }

})

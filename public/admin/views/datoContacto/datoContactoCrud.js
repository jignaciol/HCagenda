var contacts = contacts || {}

contacts.views.datoContactoCrud = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("datosContactoCrud") ),

    render: function() {
        this.$el.html(this.template())
        // coleccion de datos de contacto filtrada por usuario
        return this
    },

    initialize: function() {
        this.render()
    }

})

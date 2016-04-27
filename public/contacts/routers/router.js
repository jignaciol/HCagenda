var contacts = contacts || {}

contacts.routers.ContactsRouter = Backbone.Router.extend({

    routes: {
        "": "index"
    },

    index: function() {
        this.search = new contacts.models.search()

        var topBar = new contacts.views.top_bar_view({model: this.search})
        var listaEmpleado = new contacts.views.listaEmpleadosView({ el: $("#listaContactos"), model: this.search})
    }
})

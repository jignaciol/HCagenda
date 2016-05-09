var contacts = contacts || {}

contacts.routers.ContactsRouter = Backbone.Router.extend({

    routes: {
        "": "showContacts",
        "/": "showContacts",
    },

    showError: function(){
        new contacts.views.errorPage({el: $("#wrapper")})
    },

    showContacts: function() {
        this.search = new contacts.models.search()

        var topBar = new contacts.views.top_bar_view({model: this.search})
        var listaEmpleado = new contacts.views.listaEmpleadosView({ el: $("#listaContactos"), model: this.search})
    },

    showExtensions: function() {
        console.log("Lista de areas con sus extensiones")
        new contacts.views.listEtensionsView({ el: $("#listaContactos"), model: this.search })
    },

    showAdmin: function() {
        console.log("Pagina administratia")
    },
})

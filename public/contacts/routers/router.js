var contacts = contacts || {}

contacts.routers.ContactsRouter = Backbone.Router.extend({

    routes: {
        "": "showContacts",
        "#/contactos": "showContacts",
        "#/extensiones": "showExtensions",
        "#/admin": "showAdmin",
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
    },

    showAdmin: function() {
        console.log("Pagina administratia")
    },
})

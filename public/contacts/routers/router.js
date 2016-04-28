var contacts = contacts || {}

contacts.routers.ContactsRouter = Backbone.Router.extend({

    routes: {
        "": "showIndex",
        "#/admin": "showAdmin"
    },

    showError: function(){
        new contacts.views.errorPage({el: $("#wrapper")})
    },

    showIndex: function() {
        this.search = new contacts.models.search()

        var topBar = new contacts.views.top_bar_view({model: this.search})
        var listaEmpleado = new contacts.views.listaEmpleadosView({ el: $("#listaContactos"), model: this.search})
    },

    showAdmin: function() {
        console.log("Entra a la parte administrativa")
    }
})

(function($) {

    contacts.routers.ContactsRouter = Backbone.Router.extend({

        routes:{
            "": "showContacts",
            "extensions": "showExtensions",
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
            this.search = new contacts.models.search()

            console.log("Lista de areas con sus extensiones")
            new contacts.views.listEtensionsView({ el: $("#listaContactos") })
        },

        showAdmin: function() {
            console.log("Pagina administratia")
        },
    })

    new contacts.routers.ContactsRouter

    Backbone.emulateHTTP = true
    Backbone.emulateJSON = true
    Backbone.history.start()
})(jQuery)



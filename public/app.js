(function($) {

    contacts.routers.ContactsRouter = Backbone.Router.extend({

        routes:{
            "": "showContacts"
        },

        showError: function(){
            new contacts.views.errorPage({el: $("#wrapper")})
        },

        showContacts: function() {
            var search = new contacts.models.search();
            var topBar = new contacts.views.top_bar_view({ model: search })
            var contactBar = new contacts.views.contactBar({ el: $("#btnTabsContacts"), model: search })
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



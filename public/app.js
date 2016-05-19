(function($) {

    contacts.routers.ContactsRouter = Backbone.Router.extend({

        routes:{
            "": "showContacts"
        },

        showError: function(){
            new contacts.views.errorPage({el: $("#wrapper")})
        },

        showContacts: function() {
            contacts.app.search = new contacts.models.search();
            contacts.app.topBar = new contacts.views.top_bar_view({ model: contacts.app.search })
            contacts.app.contactBar = new contacts.views.contactBar({
                el: $("#btnTabsContacts"),
                model: contacts.app.search
            })
        },

    })

    var contactsApp = new contacts.routers.ContactsRouter()

//    Backbone.emulateHTTP = true
//    Backbone.emulateJSON = true
    Backbone.history.start()
})(jQuery)



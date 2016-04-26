var contacts = contacts || {}

contacts.routers.ContactsRouter = Backbone.Router.extend({

    routes: {
        "": "index"
    },

    index: function() {
        var gEvent = _.extend({}, Backbone.Events);

        new contacts.views.top_bar_view({gEvent: gEvent})
        new contacts.views.lista_empleados_view({gEvent: gEvent})
    }
})

var contacts = contacts || {};

contacts.views.top_bar_view = Backbone.View.extend({

    el: "#navbar",

    keyupRead: function() {
        this.gevent.trigger("leerPalabraFor");
    },

    initialize: function(options) {
       this.gevent = options.gEvent;
    },

    events: {
        "keyup #searchBox" : "keyupRead"
    }

});

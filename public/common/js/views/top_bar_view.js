var contacts = contacts || {};

contacts.views.top_bar_view = Backbone.View.extend({

    el: "#navbar",

    keyupRead: function() {
        this.model.set({word: this.$("#searchBox").val()})
        this.model.save()
    },

    initialize: function() {
       new contacts.views.formLoginView( {el: this.$("#login-dp")})
    },

    events: {
        "keyup #searchBox" : "keyupRead"
    }

});

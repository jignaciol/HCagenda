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

    doLogin: function(){
        console.log("doing login ...")
        username = this.$(".input-email").val()
        password = this.$(".input-password").val()

        console.log(username)
        console.log(password)
        doLogin = $.ajax({
            url: "/login",
            method: "POST",
            data: { username: username, password: password }
        })

        doLogin.done(function(options){
            if (options.status){
                console.log("Logeado")
            } else {
                console.log("usuario o clave invalidos")
            }
        })
    },

    events: {
        "keyup #searchBox" : "keyupRead",
        "click .btn-ingresar": "doLogin"
    }

});

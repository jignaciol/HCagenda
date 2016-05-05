var contacts = contacts || {};

contacts.views.top_bar_view = Backbone.View.extend({

    el: "#navbar",

    keyupRead: function() {
        this.model.set({word: this.$("#searchBox").val()})
        this.model.save()
    },

    initialize: function() {
        self = this
        check_login = $.ajax({
            url: "/getUsername",
            method: "POST",
            data: {username: "jignaciol@gmail.com"}
        })
        check_login.done(function(response){
            console.log(response)
        })
        /*
        ver cookie_name = $.cookie("beaker.session.id")
        if (cookie_name) {
            console.log(response)
            new contacts.views.SuccessLogin({el: self.$("#navlogin")})
        }else{
            console.log(response)
            new contacts.views.formLoginView({el: $("#login-dp")})
        }
        */
        new contacts.views.formLoginView({el: $("#login-dp")})

    },

    doLogin: function(){
        self = this
        username = this.$(".input-email").val()
        password = this.$(".input-password").val()

        doLogin = $.ajax({
            url: "/login",
            method: "POST",
            data: { username: username, password: password }
        })

        doLogin.done(function(response){
            if (response.OK){
                new  contacts.views.SuccessLogin({el: self.$("#navlogin")})
            } else {
                new contacts.views.formLoginView({el: $("#login-dp")})
            }
        })
    },

    events: {
        "keyup #searchBox" : "keyupRead",
        "click .btn-ingresar": "doLogin"
    }

})

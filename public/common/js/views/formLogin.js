var contacts = contacts || {}

contacts.views.formLoginView = Backbone.View.extend({

    tagName: "li",

    className: "dropdown",

    events: {

    },

    template: _.template( $("#formLogin").html() ),

    render: function() {
        this.$el.html( this.template())
        return this
    },

    initialize: function() {
        this.render()
    }

})

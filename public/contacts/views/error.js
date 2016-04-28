contacts = contacts || {}

contacts.views.errorPage = Backbone.View.extend({

    template: _.template( $("#tplErrorPage").html()),

    render: function() {
        this.$el.html( this.template() )
        return this
    },

    initialize: function() {
        this.render()
    }

})

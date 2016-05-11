var contacts = contacts || {}

contacts.views.menuView = Backbone.View.extend({

    events: {

    },

    template: _.template( contacts.utils.loadHtmlTemplate("menuPrincipal") ),

    render: function(){
        this.$el.html( this.template() )
        return this
    },

    initialize: function() {
        console.log(this.$el)
        this.render()
    }

})

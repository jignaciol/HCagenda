var contacts = contacts || {}

contacts.views.SuccessLogin = Backbone.View.extend({

    tagName: "li",

    className: "dropdown",

    events: {},

    template: _.template( contacts.utils.loadHtmlTemplate("SuccessLogin") ),

    render: function(){
        this.$el.html( this.template() )
        return this
    },

    initialize: function() {
        this.render()
    }

})

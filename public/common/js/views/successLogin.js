var contacts = contacts || {}

contacts.views.SuccessLogin = Backbone.View.extend({

    tagName: "li",

    className: "dropdown",

    events: {},

    template: _.template( $("#tplSuccessLogin").html() ),

    render: function(){
        this.$el.html( this.template() )
        return this
    },

    initialize: function() {
        this.render()
    }

})

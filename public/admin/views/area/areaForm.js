var contacts = contacts || {}

contacts.views.areaForm = Backbone.View.extend({

    events: {
        "click .btn-agrega-area": "addArea"
    },

    addArea: function() {

    },

    template: _.template( contacts.utils.loadHtmlTemplate("areaForm") ),

    render: function() {
        this.$el.html( this.template() )
        return this
    },

    initialize: function() {
        this.render()
    }

})

var contacts = contacts || {}

contacts.views.crudArea = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("CrudArea") ),

    render: function() {
        this.$el.html( this.template() )
        this.collection = new contacts.collections.listaArea()
        var areaForm = new contacts.views.areaForm({ el: this.$("#AreaForm"), collection: this.collection })
        var areaList = new contacts.views.areaList({ el: this.$("#AreaListBody"), collection: this.collection })
    },

    initialize: function() {
        this.render()
    },

    dispose: function() {
        this.off()
    }

})

var contacts = contacts || {}

contacts.views.crudDepartamento = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("departamentoCrud") ),

    render: function() {
        this.$el.html( this.template() )
        this.collection = new contacts.collections.listaDepartamento()
        var departamentoForm = new contacts.views.departamentoForm({ el: this.$("#AreaForm"), collection: this.collection })
        var departamentoList = new contacts.views.departamentoList({ el: this.$("#AreaListBody"), collection: this.collection })
    },

    initialize: function() {
        this.render()
    },

    dispose: function() {
        this.off()
    }

})

var contacts = contacts || {};

contacts.views.crudTipoArea = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("CrudTipoArea") ),

    render: function() {
        this.$el.html( this.template() )
        this.collection = new contacts.collections.lista_tipo_area()
        var tipoAreaList = new contacts.views.TipoAreaList({ el: this.$("#tipoAreaListBody"), collection: this.collection })
        var tipoAreaForm = new contacts.views.tipoAreaForm({ el: this.$("#tipoAreaForm"), collection: this.collection })
    },

    initialize: function(options) {
        this.render()
    },

    dispose: function() {

        this.off()

    }

});

var app = app || {};

app.views.crudTipoArea = Backbone.View.extend({

    el: $("#crudTipoArea"),

    template: _.template( $("#tplCrudTipoArea").html() ),

    render: function() {
        this.$el.html( this.template() )
        this.collection = new app.collections.lista_tipo_area()

        var tipoAreaList = new app.views.TipoAreaList({ el: this.$("#tipoAreaListBody"), collection: this.collection })
        var tipoAreaForm = new app.views.tipoAreaForm({ el: this.$("#tipoAreaForm"), collection: this.collection })
    },

    initialize: function(options) {
        this.render()
    }

});

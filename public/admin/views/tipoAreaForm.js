var app = app || {};

app.views.tipoAreaForm = Backbone.View.extend({

    events: {
        "click .btn-agrega-area": "addTipoArea"
    },

    addTipoArea: function() {
        self = this;
        var descripcion = this.$(".input-desc-area").val();
        var bl = this.$(".select-area-bl").val();
        var fec_ing = new Date().toJSON().slice(0, 10)
        var tipo_area = new app.models.tipo_area();
        tipo_area.set({"descripcion": descripcion, "bl": bl, "fec_ing": fec_ing});
        this.collection.add(tipo_area)
        console.log(this.collection)
        tipo_area.save()
    },

    template: _.template( $("#tplTipoAreaForm").html() ),

    render: function() {
        this.$el.html( this.template() );
        return this;
    },

    initialize: function() {
        this.render();
    }

});

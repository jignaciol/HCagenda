var contacts = contacts || {};

contacts.views.tipoAreaForm = Backbone.View.extend({

    events: {
        "click .btn-agrega-tipoArea": "addTipoArea"
    },

    addTipoArea: function() {
        self = this;
        var descripcion = this.$(".input-desc-tipoArea").val();
        var bl = this.$(".select-tipoArea-bl").val();
        var fec_ing = new Date().toJSON().slice(0, 10)
        var tipo_area = new contacts.models.tipoArea();
        tipo_area.set({"descripcion": descripcion, "bl": bl, "fec_ing": fec_ing});
        this.collection.add(tipo_area)
        console.log(this.collection)
        tipo_area.save()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("TipoAreaForm") ),

    render: function() {
        this.$el.html( this.template() );
        return this;
    },

    initialize: function() {
        this.render();
    }

});

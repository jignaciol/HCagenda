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

        tipoArea = new contacts.models.tipoArea()
        tipoArea.set({'descripcion': descripcion})
        tipoArea.set({'fec_ing': fec_ing})
        tipoArea.set({'bl': bl})

        tipoArea.save().done(function(response){
            id = response['id']
            tipoArea.set({id: id })
            self.collection.add(tipoArea)
        })

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

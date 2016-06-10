var contacts = contacts || {};

contacts.views.tipoAreaForm = Backbone.View.extend({

    events: {
        "click .btn-agrega-tipoArea": "addTipoArea"
    },

    addTipoArea: function() {
        self = this;
        var descripcion = this.$(".input-desc-tipoArea").val()
        var bl = this.$(".select-bl").val()
        var estado = this.$(".select-bl option:selected").html()
        var fec_ing = new Date().toJSON().slice(0, 10)

        tipoArea = new contacts.models.tipoArea()
        tipoArea.set({
            descripcion: descripcion,
            fec_ing: fec_ing,
            bl: bl,
            estado: estado
        })

        tipoArea.save().done(function(response){
            id = response['id']
            tipoArea.set({id: id })
            self.collection.add(tipoArea)
        })

    },

    template: _.template( contacts.utils.loadHtmlTemplate("TipoAreaForm") ),

    render: function() {
        this.$el.html( this.template() )
        contacts.utils.loadSelectBL(0, "enable", this.$(".select-tipoArea-bl"))
        return this;
    },

    initialize: function() {
        this.render();
    }

});

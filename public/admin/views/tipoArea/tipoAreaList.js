var contacts = contacts || {};

contacts.views.TipoAreaList = Backbone.View.extend({

    render_tipo_area: function(tipo_area){
        var tipoAreaReg = new contacts.views.TipoAreaReg({
            model: tipo_area
        })
        this.$el.append(tipoAreaReg.render().el);
    },

    render: function(){
        this.$el.html("")
        this.collection.on('add', this.render, this)
        this.collection.on('remove', this.render, this)
        this.collection.on('change', this.render, this)

        self = this
        console.log(this.collection)
        this.collection.forEach(function(tipo_area){
            self.render_tipo_area(tipo_area)
        })
    },

    ActualizarLista: function() {
        this.render()
    },

    reloadData: function() {
        self = this;
        this.collection.fetch({
            success: function() {
                self.render();
            }
        });
    },

    initialize: function() {
        self = this;
        this.collection.fetch({
            success: function() {
                self.render();
            }
        });
    }

});

var app = app || {};

app.views.TipoAreaList = Backbone.View.extend({

    render_tipo_area: function(tipo_area){
        var tipoAreaReg = new app.views.TipoAreaReg({
            model: tipo_area
        })
        this.$el.append(tipoAreaReg.render().el);
    },

    render: function(){
        this.$el.html('')
        self = this;
        this.collection.forEach(function(tipo_area){
            self.render_tipo_area(tipo_area)
        })
    },

    ActualizarLista: function() {
        this.render()
    },

    initialize: function() {
        this.collection.on('add', this.render, this)
        this.collection.on('remove', this.render, this)
        this.collection.on('change', this.render, this)

        self = this;
        this.collection.fetch({
            success: function() {
                self.render();
            }
        });
    }

});

var contacts = contacts || {}

contacts.views.departamentoList = Backbone.View.extend({

    render_departamento: function(departamento) {
        var departamentoReg = new contacts.views.departamentoReg({
            model: departamento
        })
        this.$el.append(departamentoReg.render().el)
    },

    render: function() {
        this.$el.html("")
        self = this
        this.collection.forEach(function(departamento){
            self.render_departamento(departamento)
        })
    },

    actualizarLista: function() {
        this.render()
    },

    reloadData: function() {
        self = this
        this.collection.fetch({
            succsess: function() {
                self.render()
            }
        })
    },

    initialize: function() {
        this.collection.on("add", this.render, this)
        this.collection.on("remove", this.render, this)
        this.collection.on("change", this.render, this)
        self = this
        this.collection.fetch({
            succsess: function() {
                self.render()
            }
        })
    }

})

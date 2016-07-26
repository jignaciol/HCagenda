var contacts = contacts || {}

contacts.views.datoContactoList = Backbone.View.extend({

    renderDatoContacto: function(datoContacto) {
        var datoContactoReg = new contacts.views.datoContactoReg({
            model: datoContacto
        })
        this.$el.append(datoContactoReg.render().el)
    },

    render: function() {
        this.$el.html("")
        self=this
        this.collection.forEach(function(datoContacto){
            self.renderDatoContacto(datoContacto)
        })
    },

    initialize: function() {
        this.collection.on("add", this.render, this)
        this.collection.on("remove", this.render, this)
        this.collection.on("change", this.render, this)

        this.render()
    }

})

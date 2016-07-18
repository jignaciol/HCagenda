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
        this.collection.on("add", this.render, this)
        this.collection.on("remove", this.render, this)
        this.collection.on("change", this.render, this)

        self=this
        this.collection.forEach(function(datoContacto){
            self.renderDatoContacto(datoContacto)
        })
    },

    reloadData: function() {
        self=this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    },

    renderFilter: function(cfiltered){
        this.$el.html("")
        self=this
        cfiltered.forEach(function(empleado){
            self.renderEmpleado(empleado)
        })
    },

    leerPalabraFor: function() {
        self=this
        this.collection.fetch({
            success: function() {
                //var filterWord = self.model.get("word")
                //var cfiltered = self.collection.searchByName(filterWord)
                //self.renderFilter(cfiltered)
            }
        })
    },

    initialize: function() {
        //this.model.on("change", this.leerPalabraFor, this)
        self=this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    }

})

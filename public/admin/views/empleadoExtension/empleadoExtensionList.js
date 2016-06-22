var contacts = contacts || {}

contacts.views.empleadoExtensionList = Backbone.View.extend({

    renderAsignacion: function(empleadoExtension) {
        var empleadoExtensionReg = new contacts.views.empleadoExtensionReg({
            model: empleadoExtension
        })
        this.$el.append(empleadoExtensionReg.render().el)
    },

    render: function() {
        this.$el.html("")
        this.collection.on("add", this.render, this)
        this.collection.on("remove", this.render, this)
        this.collection.on("change", this.render, this)
        self=this
        this.collection.forEach(function(empleadoExtension){
            self.renderAsignacion(empleadoExtension)
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

    initialize: function(){
        self=this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    }

})

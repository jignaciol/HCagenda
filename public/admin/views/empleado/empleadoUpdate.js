var contacts = contacts || {}

contacts.views.empleadoUpdate = Backbone.View.extend({

    events: {
        "click .btn-cancel": "cancel",
        "click .btn-update": "update"
    },

    update: function() {
        self = this
        this.model.set({ })
        this.model.save().done(function(){
            self.cancel()
        })
    },

    cancel: function() {
        $("#formEmpleado").modal("hide")
        $(".modal-backdrop").remove()
        contacts.app.extensionUpdate = null
        this.dispose()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("empleadoUpdate") ),

    render: function() {
        console.log("renderizando formulario de actualizacion")
        this.$el.html( this.template( this.model.toJSON() ) )
        console.log(this.template)
        $("#modalFormEmpleado").modal({backdrop: 'static'})
        return this
    },

    dispose: function() {
        this.undelegateEvents()
        this.off()
        this.$el.removeData().unbind()
    },

    initialize: function() {
        this.render()
    }

})

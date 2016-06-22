var contacts = contacts || {}

contacts.views.empleadoForm = Backbone.View.extend({

    template: _.template( contacts.utils.loadHtmlTemplate("empleadoForm") ),

    events: {
        "click .btn-add": "addEmpleado",
        "click .btn-cancel": "cancel"
    },

    cancel: function() {
       this.$("#formEmpleado").modal("hide")
       $(".modal-backdrop").remove()
       contacts.app.formEmpleado = null
       this.dispose()
    },

    dispose: function() {
       this.undelegateEvents()
       this.off()
       this.$el.removeData().unbind()
    },

    addEmpleado: function() {

    },

    render: function() {
        this.$el.html(this.template())
        this.$("#formEmpleado").modal({backdrop: 'static'})
        return this
    },

    initialize: function() {
        this.render()
    }

})

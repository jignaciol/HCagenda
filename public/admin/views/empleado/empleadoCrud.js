var contacts = contacts || {}

contacts.views.empleadoCrud = Backbone.View.extend({

   template: _.template( contacts.utils.loadHtmlTemplate("empleadoCrud") ),

   events: {
        "click .btn-add": "addEmpleado"
   },

   addEmpleado: function() {
       contacts.app.formEmpleado = new contacts.views.empleadoForm({ el: this.$("#formEmpleado"), collection: this.collection })
   },

   render: function(){
       this.$el.html(this.template())
       var empleadoList = new contacts.views.empleadoList({
               el: this.$("#listBody"),
               collection: this.collection,
               model: contacts.app.search
           })
   },

   initialize: function(){
        this.render()
   },

   dispose: function() {
        this.off()
   }

})

var contacts = contacts || {}

contacts.views.empleadoExtensionCrud = Backbone.View.extend({

   template: _.template( contacts.utils.loadHtmlTemplate("empleadoExtensionCrud") ),

   render: function(){
       this.$el.html(this.template())
       this.collection = new contacts.collections.listaExtensionesAsignadas()
       var eextensionForm = new contacts.views.empleadoExtensionForm({ el: this.$(".form-eextension"), collection: this.collection })
       var eextensionList = new contacts.views.empleadoExtensionList({ el: this.$("#listBody"), collection: this.collection })
   },

   initialize: function(){
        this.render()
   },

   dispose: function() {
        this.off()
   }

})

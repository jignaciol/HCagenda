var contacts = contacts || {}

contacts.views.extensionesCrud = Backbone.View.extend({

   template: _.template( contacts.utils.loadHtmlTemplate("extensionesCrud") ),

   events: {
       "click .btn-add-extension": "addExtension"
   },

   addExtension: function() {
       contacts.app.formExtension = new contacts.views.extensionForm({ el: this.$("#formBody"), collection: this.collection })
   },

   render: function(){
       this.$el.html(this.template())
       this.collection = new contacts.collections.extensionList()
       var extensionList = new contacts.views.extensionListView({ el: this.$("#listBody"), collection: this.collection })
   },

   initialize: function(){
        this.render()
   },

})

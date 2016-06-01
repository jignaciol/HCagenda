var contacts = contacts || {}

contacts.views.extensionesCrud = Backbone.View.extend({

   template: _.template(contacts.utils.loadHtmlTemplate("extensionesCrud")),

   render: function(){
        this.$el.html(this.template())
   },

   initialize: function(){
        this.render()
   },

   dispose: function(){
        this.off()
   }

})

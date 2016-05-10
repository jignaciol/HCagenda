var contacts = contacts || {};

contacts.views.listExtensionsView = Backbone.View.extend({

   renderExtensionItem: function(extension){
        var extensionView = new contacts.views.ExtensionsView({ model: extension });
        this.$el.append(extensionView.render().el);
   },

   render: function(){
       this.$el.html("");
       self = this;
       this.collection.forEach(function(extension){
           self.renderExtensionItem(extension);
       });
   },

   renderFilter: function(cfiltered){
        this.$el.html("");
        self = this;
        cfiltered.forEach(function(extension){
            self.renderExtensionItem(extension);
        });
   },

   leerPalabraFor: function(){
       self = this;
       this.collection.fetch({
           success: function() {
               var filterWord = self.model.get("word")
               var cfiltered = self.collection.searchByName(filterWord)
               self.renderFilter(cfiltered)
            }
       });
   },

   initialize: function() {
       this.model.on("change", this.leerPalabraFor, this)

       self = this;
       this.collection = new contacts.collections.listExtensions();
       this.collection.fetch({
           success: function() {
               self.render();
           }
       });
   },

   dispose: function() {

       //this.remove()

       this.off()

       this.model.off(null, null, this)

    }

});

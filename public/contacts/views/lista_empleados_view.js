var contacts = contacts || {};

contacts.views.listaEmpleadosView = Backbone.View.extend({

   render_empleado: function(empleado){
        var empleado_view = new contacts.views.empleado_view({
            model: empleado
        });
        this.$el.append(empleado_view.render().el);
   },

   render: function(){
       this.$el.html("");
       self = this;
       this.collection.forEach(function(empleado){
           self.render_empleado(empleado);
       });
   },

   renderFilter: function(cfiltered){
        this.$el.html("");
        self = this;
        cfiltered.forEach(function(empleado){
            self.render_empleado(empleado);
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
       this.collection = new contacts.collections.lista_empleados();
       this.collection.fetch({
           success: function() {
               self.render();
           }
       });
   }

});

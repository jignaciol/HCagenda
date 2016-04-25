var contacts = contacts || {};

contacts.views.lista_empleados_view = Backbone.View.extend({

   el: $("#listaContactos"),

   render_empleado: function(empleado){
       console.log("instanciando vista")
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
        this.$el.html('');
        self = this;
        cfiltered.forEach(function(empleado){
            self.render_empleado(empleado);
        });
   },

   leerPalabraFor: function(){
       self = this;
       this.collection.fetch({
           success: function() {
               var filterWord = $("#searchBox").val();
               var cfiltered = self.collection.searchByName(filterWord);
               self.renderFilter(cfiltered);
            }
       });
   },

   initialize: function(options) {
       this.gevent = options.gEvent;
       _.bindAll(this, "leerPalabraFor");
       this.gevent.bind("leerPalabraFor", this.leerPalabraFor);

       self = this;
       this.collection = new contacts.collections.lista_empleados();
       this.collection.fetch({
           success: function() {
               self.render();
           }
       });
   }

});

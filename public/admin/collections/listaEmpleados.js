var contacts = contacts || {}

contacts.collections.listaEmpleados = Backbone.Collection.extend({

    url: "/api/empleado",

    model: contacts.models.empleado,

    searchByName: function(letters){
        if (letters == "") return this;

        var pattern = new RegExp(letters,"ig");

        return _(this.filter(function(empleado){
            return pattern.test(empleado.get('nombre') + empleado.get('apellido'));
        }));
    }
})

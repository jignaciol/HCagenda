var contacts = contacts || {};

contacts.collections.lista_empleados = Backbone.Collection.extend({

    url: 'empleado/',

    model: contacts.models.empleado,

    searchByName: function(letters){
        if (letters == "") return this;

        var pattern = new RegExp(letters,"ig");

        return _(this.filter(function(empleado){
            return pattern.test(empleado.get('nombre') + empleado.get('apellido') + empleado.get('telefono'));
        }));
    }
});

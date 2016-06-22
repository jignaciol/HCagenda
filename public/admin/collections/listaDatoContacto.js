var contacts = contacts || {}

contacts.collections.listaDatoContacto = Backbone.Collection.extend({

    url: "/api/datocontacto",

    model: contacts.models.datoContacto,

    filterByEmpleado: function() {
        if (letters == "") return this;

        var pattern = new RegExp(letters,"ig");

        return _(this.filter(function(datoContacto){
            return pattern.test(datoContacto.get("id_empleado"));
        }));
    }

})

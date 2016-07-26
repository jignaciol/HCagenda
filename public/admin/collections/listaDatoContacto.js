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
    },

    getFilteredList: function(id) {
        var filtered = new Backbone.Collection(this.filter(function(model) {
            return model.get('id_empleado') == id
        }))
        console.log(filtered)
        return filtered
    }
})

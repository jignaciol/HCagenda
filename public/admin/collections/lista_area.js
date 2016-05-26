var contacts = contacts || {}

 contacts.collections.listaArea = Backbone.Collection.extend({

    url: "/api/area",

    model: contacts.models.area,

    filterByTipo: function(tipo_area){
        if (tipo_area == 0) return this

        var pattern = new RegExp(tipo_area,"ig")

        return _(this.filter(function(area){
            return area.get('id_tipo_area') == tipo_area
        }));
    }

 })

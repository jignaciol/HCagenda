var contacts = contacts || {}

contacts.models.area = Backbone.Model.extend({

    url: "/api/area",

    defaults: {
        descripcion: "",
        fec_ing: "",
        tipo_area: "",
        bl: 1
    },

    /*
    relations: [
        {
            type: Backbone.HasOne,
            key: "id_tipo_area",
            relatedModel: contacts.models.tipoarea,
            reverseRelation: {
                key: "id",
                includeInJSON: "id"
            }
        }
    ]
    */

})

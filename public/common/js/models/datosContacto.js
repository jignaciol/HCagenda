var contacts = contacts || {}

contacts.models.datosContacto = Backbone.Model.extend({

    url: "api/datoscontacto",

    defaults: {
        descripcion: "",
        fec_ing: ""
    },

    relations: [
        {
            type: Backbone.HasOne,
            key: "id_empleado",
            relatedModel: contacts.models.empleado,
            reverseRelation: {
                key: "id",
                includeInJSON: "id"
            }
        },
        {
            type: Backbone.HasOne,
            key: "id_tipo_contacto",
            relatedModel: contacts.models.tipoDatoContacto,
            reverseRelation: {
                key: "id",
                includeInJSON: "id"
            }
        }
    ]
})

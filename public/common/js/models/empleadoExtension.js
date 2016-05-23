var contacts = contacts || {}

contacts.models.empleadoExtension = Backbone.Model.extend({

    url: "api/empleadoextension",

    defaults: {
        fec_asignacion: "",
        mostrar: ""
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
            key: "id_extension",
            relatedModel: contacts.models.extension,
            reverseRelation: {
                key: "id",
                includeInJSON: "id"
            }
        }
    ]
})

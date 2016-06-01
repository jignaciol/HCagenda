var contacts = contacts || {}

contacts.views.departamentoReg = Backbone.View.extend({

    tagName: "li",

    className: "list-group-item",

    events: {
        "click .edit-dpto": "edit",
        "click .delete-dpto": "delete",
        "click .update-dpto": "update",
        "click .cancel-dpto": "cancel",
    },

    edit: function() {
        this.$(".edit-dpto").hide()
        this.$(".delete-dpto").hide()
        this.$(".update-dpto").show()
        this.$(".cancel-dpto").show()

        var descripcion = this.$('.descripcion').html()

        objetivo = this.$(".ubicacion")
        id_ubicacion = this.model.get("id_ubicacion")
        contacts.utils.loadSelectArea(id_ubicacion, "enable", objetivo, 1)

        objetivo = this.$(".piso")
        id_piso = this.model.get("id_piso")
        contacts.utils.loadSelectArea(id_piso, "enable", objetivo, 2)

        objetivo = this.$(".estado")
        bl = this.model.get("bl")
        contacts.utils.loadSelectBL(bl, "enable", objetivo, 2)

        this.$('.descripcion').html('<input name="descripcion" type="text" class="form-control descripcion-update small" value="' + descripcion + '">');

    },

    cancel: function() {
        this.render()
    },

    update: function() {
        self = this
        this.model.set({
            descripcion: this.$(".descripcion-update").val(),
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html(),
            id_piso: this.$(".select-ubicacion_2").val(),
            piso: this.$(".select-ubicacion_2 option:selected").html(),
            alias: "",
            id_ubicacion: this.$(".select-ubicacion_1").val(),
            ubicacion: this.$(".select-ubicacion_1 option:selected").html()
        })
        this.model.save({
            success: function() {
                self.render()
            }
        })
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("departamentoReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initialize: function() {
        this.render()
    }

})

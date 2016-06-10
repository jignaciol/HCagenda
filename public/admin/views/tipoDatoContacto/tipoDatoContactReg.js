var contacts = contacts || {}

contacts.views.tipoDatoContactoReg = Backbone.View.extend({

    tagName: "li",

    className: "list-group-item",

    events: {
        'click .edit-tipoDatoC': 'edit',
        'click .delete-tipoDatoC': 'delete',
        'click .update-tipoDatoC': 'update',
        'click .cancel-tipoDatoC': 'cancel'
    },

    edit: function() {
        this.$('.edit-tipoDatoC').hide();
        this.$('.delete-tipoDatoC').hide();
        this.$('.update-tipoDatoC').show();
        this.$('.cancel-tipoDatoC').show();

        var descripcion = this.$('.descripcion-tipoDatoC').html();

        this.$('.descripcion-tipoDatoC').html('<input name="descripcion" type="text" class="form-control descripcion-update" value="' + descripcion + '">');
        contacts.utils.loadSelectBL(this.model.get("bl") , "enable", this.$(".estado-tipoDC"))
    },

    cancel: function() {
        this.render()
    },

    update: function() {
        self = this
        this.model.set({
            descripcion: this.$(".descripcion-update").val(),
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html()
        })
        this.model.save({}, {
            success: function(){
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

    template: _.template( contacts.utils.loadHtmlTemplate("TipoDatoContactoReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ) )
        return this
    },

    initialize: function() {
        this.render()
    }
})

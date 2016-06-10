var contacts = contacts || {};

contacts.views.TipoAreaReg = Backbone.View.extend({

    tagName: "li",

    className: "list-group-item",

    events: {
        'click .edit-tipoArea': 'edit',
        'click .delete-tipoArea': 'delete',
        'click .update-tipoArea': 'update',
        'click .cancel-tipoArea': 'cancel'
    },

    edit: function() {
        this.$('.edit-tipoArea').hide();
        this.$('.delete-tipoArea').hide();
        this.$('.update-tipoArea').show();
        this.$('.cancel-tipoArea').show();

        var descripcion = this.$('.descripcion-tipoArea').html();

        this.$('.descripcion-tipoArea').html('<input name="descripcion" type="text" class="form-control descripcion-update" value="' + descripcion + '">');
        contacts.utils.loadSelectBL( this.model.get("bl"), "enable", this.$(".estado-tipoArea"))
    },

    cancel: function() {
        this.render();
    },

    update: function() {
        var self = this;
        this.model.set({
            descripcion: this.$('.descripcion-update').val(),
            bl: this.$(".select-bl").val(),
            estado: this.$(".select-bl option:selected").html()
        })
        this.model.save({}, {
            success: function(){
                self.render();
            }
        });
    },

    delete: function() {
        this.model.destroy({
            data: this.model.id,
            contentType: "application/json"
        })
        this.render()
    },

    template: _.template( contacts.utils.loadHtmlTemplate("TipoAreaReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ) );
        return this;
    },

    initialize: function() {
        this.render();
    }

});

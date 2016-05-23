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
        if (this.model.get('bl') == 0) {
            this.$('.estado-tipoArea').html('<select name="bl" class="form-control data-estado"> <option value="0" selected="selected">Oculto</option> <option value="1">Visible</option> </select>');
        } else {
            this.$('.estado-tipoArea').html('<select name="bl" class="form-control data-estado"> <option value="0">Oculto</option> <option value="1" selected="selected">Visible</option> </select>');
        }
    },

    cancel: function() {
        this.render();
    },

    update: function() {
        var self = this;
        this.model.set({
            'descripcion': this.$('.descripcion-update').val(),
            'bl': this.$('.data-estado').val()
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

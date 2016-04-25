var app = app || {};

app.views.TipoAreaReg = Backbone.View.extend({

    tagName: "li",

    className: "list-group-item",

    events: {
        'click .edit-area': 'edit',
        'click .delete-area': 'delete',
        'click .update-area': 'update',
        'click .cancel-area': 'cancel'
    },

    edit: function() {
        this.render();
        this.$('.edit-area').hide();
        this.$('.delete-area').hide();
        this.$('.update-area').show();
        this.$('.cancel-area').show();

        var descripcion = this.$('.descripcion-area').html();

        this.$('.descripcion-area').html('<input name="descripcion" type="text" class="form-control descripcion-update" value="' + descripcion + '">');
        if (this.model.get('bl') == 0) {
            this.$('.estado-area').html('<select name="bl" class="form-control data-estado-area"> <option value="0" selected="selected">Oculto</option> <option value="1">Visible</option> </select>');
        } else {
            this.$('.estado-area').html('<select name="bl" class="form-control data-estado-area"> <option value="0">Oculto</option> <option value="1" selected="selected">Visible</option> </select>');
        }
    },

    cancel: function() {
        this.render();
    },

    update: function() {
        var self = this;
        this.model.set('descripcion', this.$('.descripcion-update').val());
        this.model.set('bl', this.$('.data-estado-area').val());
        this.model.save({}, {
            success: function(){
                self.render();
            }
        });
    },

    delete: function() {
        this.model.destroy()
    },

    template: _.template( $("#tplTipoAreaReg").html() ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ) );
        return this;
    },

    initialize: function() {
        this.render();
    }

});

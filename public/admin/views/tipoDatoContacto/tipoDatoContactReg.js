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
        if (this.model.get('bl') == 0) {
            this.$('.estado-tipoDatoC').html('<select name="bl" class="form-control data-estado"> <option value="0" selected="selected">Oculto</option> <option value="1">Visible</option> </select>');
        } else {
            this.$('.estado-tipoDatoC').html('<select name="bl" class="form-control data-estado"> <option value="0">Oculto</option> <option value="1" selected="selected">Visible</option> </select>');
        }

    },

    cancel: function() {
        this.render()
    },

    update: function() {
        self = this
        this.model.set({
            'descripcion': this.$('.descripcion-update').val(),
            'bl': this.$('.data-estado').val()
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

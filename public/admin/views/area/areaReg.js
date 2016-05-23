var contacts = contacts || {}

contacts.views.areaReg = Backbone.View.extend({

    tagName: "li",

    className: "list-group-item",

    events: {
        "click .edit-area": "edit",
        "click .delete-area": "delete",
        "click .update-area": "update",
        "click .cancel-area": "cancel",
    },

    edit: function() {
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
        this.render()
    },

    update: function() {
        self = this
        this.model.set({
            "descripcion": this.$(".descripcion-update").val(),
            "bl": this.$(".data-estado").val()
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

    template: _.template( contacts.utils.loadHtmlTemplate("AreaReg") ),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ))
        return this
    },

    initialize: function() {
        this.render()
    }

})

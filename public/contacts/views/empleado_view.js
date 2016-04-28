var contacts = contacts || {};

contacts.views.empleado_view = Backbone.View.extend({

    tagName : "li",

    className: "contactItem",

    events: {
        "click .mostrar-detalles": "mostrarDetalles"
    },

    template: _.template( $("#empleado-template").html() ),

    render: function() {
        //this.url = "fotos/F00" + this.model.get("ficha") + '.jpg';
        this.url_tested = contacts.utils.checkImgUrl(this.model.get("ficha"));

        /* Agrego una variable url_tested al modelo */
        this.model.set({url_tested: this.url_tested});
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    },

    mostrarDetalles: function(e) {
        $(e.target).parent().parent().toggleClass("seleccionado");
        $(e.target).parent().parent().parent().find(".detalles").toggleClass('activo');
        $(e.target).parent().parent().parent().find('.detalles').slideToggle('fast');
    },

    dispose: function() {

        // same as this.$el.remove()
        this.remove()

        // unbind events that are set on this view
        this.off()

        // remove all models bindings made by this view
        this.model.off( null, null, this)

    },

    initialize: function() {
        this.render();
    }

});

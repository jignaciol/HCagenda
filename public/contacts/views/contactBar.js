var contacts = contacts || {}

contacts.views.contactBar = Backbone.View.extend({

    tagName: "div",

    className: "row",

    events: {
        "click .btnContacts": "showContacts",
        "click .btnExtensions": "showExtensions"
    },

    showContacts: function() {
        if(this.extensions){
            this.extensions.dispose()
        }
        $("#searchBox").val("")
        this.contacts = new contacts.views.listaEmpleadosView({ el: this.$(".panel-body"), model: this.model})
    },

    showExtensions: function() {
        if(this.contacts){
            this.contacts.dispose()
        }
        $("#searchBox").val("")
        this.extensions =  new contacts.views.listExtensionsView({el: this.$(".panel-body"), model: this.model})
    },

    template: _.template( contacts.utils.loadHtmlTemplate("BtnContactos") ),

    render: function() {
        this.$el.html( this.template());
        return this;
    },

    dispose: function() {

        // same as this.$el.remove()
        //this.remove()

        // unbind events that are set on this view
        this.off()

        // remove all models bindings made by this view
        this.model.off( null, null, this)

    },

    initialize: function() {
        this.render()
        this.showContacts()
    }

})

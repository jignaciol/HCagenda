var contacts = contacts || {}

contacts.views.contactBar = Backbone.View.extend({

    tagName: "div",

    className: "row",

    events: {},

    template: _.template( $("#tplBtnContactos").html() ),

    render: function() {

    } 
})

var contacts = contacts || {}

contacts.views.menuView = Backbone.View.extend({

    events: {
        /* Referencias */
        "click .menuBtnArea": "area",
        "click .menuBtnTipoArea": "tipoArea",
        "click .menuBtnTipoDatoContacto": "tipoDatoContacto",

        /* Agenda */
        "click .menuBtnListaContactos" : "contactos",
        "click .menuBtnEmpleados": "empleados",
        "click .menuBtnAsignarExtension": "asignarExtension",
        "click .menuBtnExtensiones": "extensiones",
        "click .menuBtnDepartamentos": "departamentos",

        /* Mensajeria SMS */
        "click .menuBtnSMSindividual": "smsIndividual",
        "click .menuBtnSMSmasivo": "smsMasivo"
    },

    /* Opciones de menu */
    area: function() {
        console.log("boton areas presionado")
    },

    tipoArea: function() {
        console.log("boton tipo de area presionado")
        $("#btnTabsContacts").html("")
        contacts.app.adminArea = new contacts.views.crudTipoArea({ el: $("#adminContainer") })
    },

    tipoDatoContacto: function() {
        console.log("boton tipo dato contacto presionado")
    },

    contactos: function() {
       $("#btnTabsContacts").html("")
       $("#adminContainer").html("")

       contacts.app.contactBar = new contacts.views.contactBar({ el: $("#btnTabsContacts"), model: contacts.app.search })
       console.log("lista de contactos presionado")
    },

    empleados: function() {
        console.log("boton empleados presionado")
    },

    asignarExtension: function() {
        console.log("boton asignar extension presionado")
    },

    extensiones: function() {
        console.log("boton extensiones presionado")
    },

    departamentos: function() {
        console.log("boton departamentos presionado")
    },

    smsIndividual: function() {
        console.log("boton smsIndividual presionado")
    },

    smsMasivo: function() {
        console.log("boton smsMasivo presionado")
    },
    /* fin opciones de menu */

    template: _.template( contacts.utils.loadHtmlTemplate("menuPrincipal") ),

    render: function(){
        this.$el.html( this.template() )
        return this
    },

    initialize: function() {
        this.render()
    }

})

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
        $("#btnTabsContacts").html("")
        contacts.app.adminArea = new contacts.views.crudArea({ el: $("#adminContainer") })
    },

    tipoArea: function() {
        console.log("boton tipo de area presionado")
        $("#btnTabsContacts").html("")
        contacts.app.adminTipoArea = new contacts.views.crudTipoArea({ el: $("#adminContainer") })
    },

    tipoDatoContacto: function() {
        console.log("boton tipo dato contacto presionado")
        $("#btnTabsContacts").html("")
        contacts.app.adminDatoContacto = new contacts.views.crudDatoContacto({ el: $("#adminContainer") })
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
        $("#btnTabsContacts").html("")
        contacts.app.adminExtensiones = new contacts.views.extensionesCrud({ el: $("#adminContainer") })
    },

    departamentos: function() {
        console.log("boton departamentos presionado")
        $("#btnTabsContacts").html("")
        contacts.app.admindpto = new contacts.views.crudDepartamento({ el: $("#adminContainer") })
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

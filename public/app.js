/*
var gEvent = _.extend({}, Backbone.Events);

barra_top = new contacts.views.top_bar_view({gEvent: gEvent});
directorio = new contacts.views.lista_empleados_view({gEvent: gEvent});


edita_tipo_area = new directorio.views.crudTipoArea();

*/


$(document).ready(function(){
    router = new contacts.routers.ContactsRouter()

    Backbone.emulateHTTP = true
    Backbone.emulateJSON = true
    Backbone.history.start()
})



/*
new contacts.routers.ContactsRouter()

Backbone.emulateHTTP = true
Backbone.emulateJSON = true
Backbone.history.start()
*/

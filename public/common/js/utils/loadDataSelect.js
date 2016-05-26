var contacts = contacts || {}

contacts.utils.loadSelectTipoArea = function(seleccionado, status, objetivo){
    listaTipoArea = new contacts.collections.lista_tipo_area()

    $.when(listaTipoArea.fetch()).done(function(lista){
        html_select = "<select id='' class='form-control select-tipoArea' " + status + ">"
        lista.forEach(function(tipoArea){
            if(seleccionado == tipoArea["id"]) {
                 html_select += "<option value='" + tipoArea["id"] + "' selected='selected' >" + tipoArea["descripcion"] + "</option>"
            }else{
                html_select += "<option value='" + tipoArea["id"] + "'>" + tipoArea["descripcion"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}

contacts.utils.loadSelectUbicacion = function(seleccionado, status, objetivo){

    listaUbicacion = new contacts.collections.listaArea()

    listaUbicacion.fetch().done(function(filtered){
        html_select = "<select id='' class='form-control select-ubicacion' " + status + ">"
        filtered.forEach(function(ubicacion){
            if(seleccionado == ubicacion["id"]){
                html_select += "<option value='" + ubicacion["id"] + "' selected='selected' >" + ubicacion["descripcion"] + "</option>"
            } else {
                html_select += "<option value='" + ubicacion["id"] + "'>" + ubicacion["descripcion"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}

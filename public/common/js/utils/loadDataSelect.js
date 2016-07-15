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

contacts.utils.loadSelectArea = function(seleccionado, status, objetivo, tipoArea){

    listaAreas = new contacts.collections.listaArea()

    listaAreas.fetch().done(function(lista){
        html_select = "<select id='' class='form-control select-ubicacion_" + tipoArea + "' " + status + ">"
        lista.forEach(function(area){
            if(area["id_tipo_area"]==tipoArea){
                if(seleccionado == area["id"]){
                    html_select += "<option value='" + area["id"] + "' selected='selected' >" + area["descripcion"] + "</option>"
                } else {
                    html_select += "<option value='" + area["id"] + "'>" + area["descripcion"] + "</option>"
                }
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}

contacts.utils.loadSelectBL = function(seleccionado, status, objetivo){

    listaBL = new contacts.collections.listaBorradoLogico()

    listaBL.fetch().done(function(lista){
        html_select = "<select id='' class='form-control select-bl' " + status + ">"
        lista.forEach(function(codigo){
            if(seleccionado == codigo["id"]){
                html_select += "<option value=" + codigo["id"] + " selected='selected' >" + codigo["descripcion"] + "</option>"
            } else {
                html_select += "<option value=" + codigo["id"] + ">" + codigo["descripcion"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}

contacts.utils.loadSelectDepartamento = function(seleccionado, status, objetivo) {

    listaDepartamento = new contacts.collections.listaDepartamento()

    listaDepartamento.fetch().done(function(lista){
        html_select = "<select class='form-control select-departamento' " + status + ">"
        lista.forEach(function(codigo){
            if(seleccionado == codigo["id"]){
                html_select += "<option value=" + codigo["id"] + " selected='selected' >" + codigo["descripcion"] + "</option>"
            } else {
                html_select += "<option value=" + codigo["id"] + ">" + codigo["descripcion"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}


contacts.utils.loadSelectExtensiones = function(seleccionado, status, objetivo) {

    listaExtensiones = new contacts.collections.extensionList()

    listaExtensiones.fetch().done(function(lista){
        html_select = "<select class='form-control select-extension' " + status + ">"
        lista.forEach(function(codigo){
            if(seleccionado == codigo["id"]){
                html_select += "<option value=" + codigo["id"] + " selected='selected' >" + codigo["numero"] + "</option>"
            } else {
                html_select += "<option value=" + codigo["id"] + ">" + codigo["numero"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })
}


contacts.utils.loadSelectEmpleado = function(seleccionado, status, objetivo) {

    listaEmpleados = new contacts.collections.listaEmpleados()

    listaEmpleados.fetch().done(function(lista){
        html_select = "<select class='form-control select-empleado' " + status + ">"
        lista.forEach(function(empleado){
            if(seleccionado == empleado["id"]){
                html_select += "<option value=" + empleado["id"] + " selected='selected' >" + empleado["nombre"] + " " + empleado["apellido"] + "</option>"
            } else {
                html_select += "<option value=" + empleado["id"] + ">" + empleado["nombre"] + " " + empleado["apellido"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}


contacts.utils.loadSelectTipoDatoContacto = function(seleccionado, status, objetivo) {

    listaTipoDatoContacto = new contacts.collections.listaTipoDatoContacto()

    listaTipoDatoContacto.fetch().done(function(lista){
        html_select = "<select class='form-control select-tipoDatoContacto' " + status + ">"
        lista.forEach(function(tipoDatoContacto){
            if(seleccionado == tipoDatoContacto["id"]){
                html_select += "<option value=" + tipoDatoContacto["id"] + " selected='selected' >" + tipoDatoContacto["descripcion"] + "</option>"
            } else {
                html_select += "<option value=" + tipoDatoContacto["id"] + ">" + tipoDatoContacto["descripcion"] + "</option>"
            }
        })
        html_select += "</select>"
        $(objetivo).html(html_select)
    })

}

var contacts = contacts || {}

contacts.collections.listaEmpleadoExtension = Backbone.Collection.extend({

	url: "/api/empleadoextension",
	
	model: contacts.models.empleadoExtension
	
})

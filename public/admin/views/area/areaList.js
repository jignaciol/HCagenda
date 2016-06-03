var contacts = contacts || {}

contacts.views.areaList = Backbone.View.extend({

    render_area: function(area) {
        var areaReg = new contacts.views.areaReg({
            model: area
        })
        this.$el.append(areaReg.render().el)
    },

    render: function() {
        this.$el.html("")
        self = this
        this.collection.forEach(function(area){
            self.render_area(area)
        })
    },

    actualizarLista: function() {
        this.render()
    },

    reloadData: function() {
        self = this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    },

    initialize: function() {
        this.collection.on("add", this.render, this)
        this.collection.on("remove", this.render, this)
        this.collection.on("change", this.render, this)
        self = this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    }

})

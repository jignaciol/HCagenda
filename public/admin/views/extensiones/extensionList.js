var contacts = contacts || {}

contacts.views.extensionListView = Backbone.View.extend({

    renderExtension: function(extension) {
        var extensionReg = new contacts.views.extensionReg({
            model: extension
        })
        this.$el.append(extensionReg.render().el)
    },

    render: function() {
        this.$el.html("")
        this.collection.on("add", this.render, this)
        this.collection.on("remove", this.render, this)
        this.collection.on("change", this.render, this)
        self=this

        this.collection.forEach(function(extension){
            self.renderExtension(extension)
        })
    },

    reloadData: function() {
        self=this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    },

    initialize: function(){
        self=this
        this.collection.fetch({
            success: function() {
                self.render()
            }
        })
    }

})

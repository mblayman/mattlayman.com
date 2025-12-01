local render = require("nibiru.template").render

local responders = {}

function responders.index(request)
    return render("index.html")
end

return responders

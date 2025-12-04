local http = require("nibiru.http")
local render = require("nibiru.template").render

local responders = {}

function responders.index(request)
    return render("index.html")
end

function responders.up()
    return http.ok("ok")
end

return responders

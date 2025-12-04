local Application = require("nibiru.application")
local http = require("nibiru.http")
local Route = require("nibiru.route")

local resp = require("app.responders")

function up(request)
    return http.ok("")
end

local routes = {
    Route("/", resp.index),
    Route("/up", up),
}

return Application(routes)

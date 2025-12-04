local Application = require("nibiru.application")
local Route = require("nibiru.route")

local resp = require("app.responders")

local routes = {
    Route("/", resp.index),
    Route("/up", resp.up),
}

return Application(routes)

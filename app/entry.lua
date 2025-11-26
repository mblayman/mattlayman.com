local Application = require("nibiru.application")
local http = require("nibiru.http")
local Route = require("nibiru.route")

local function index()
    return http.ok("home")
end

local routes = {
    Route("/", index),
}

return Application(routes)

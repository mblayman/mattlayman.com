local Application = require("nibiru.application")
local Route = require("nibiru.route")

require("app.template_functions")

local resp = require("app.responders")
local blog_resp = require("app.blog.responders")
local ud_resp = require("app.understand_django.responders")

local routes = {
    Route("/", resp.index),
    Route("/up", resp.up),
    Route("/blog/{slug:string}", blog_resp.entry, "blog_entry"),
    Route(
        "/understand-django/{slug:string}",
        ud_resp.chapter,
        "understand_django_chapter"
    ),
}

return Application(routes)

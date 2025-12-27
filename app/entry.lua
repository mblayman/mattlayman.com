local Application = require("nibiru.application")
local Route = require("nibiru.route")

local blog_pages = require("app.blog.pages")
blog_pages.load()

local resp = require("app.responders")
local blog_resp = require("app.blog.responders")

local routes = {
    Route("/", resp.index),
    Route("/up", resp.up),
    Route("/blog/{slug:string}", blog_resp.entry, "blog_entry"),
}

return Application(routes)

local http = require("nibiru.http")
local render = require("nibiru.template").render

local blog_pages = require("app.blog.pages")

local responders = {}

function responders.index(request)
    return render("index.html", { pages = blog_pages.list_by_date() })
end

function responders.up()
    return http.ok("ok")
end

return responders

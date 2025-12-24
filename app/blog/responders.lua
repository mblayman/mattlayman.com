local http = require("nibiru.http")
local render = require("nibiru.template").render

local pages = require("app.blog.pages")

local responders = {}

function responders.entry(request, slug)
    local page = pages.get(slug)
    if page then
        return render("blog/entry.html", page)
    else
        return http.not_found()
    end
end

return responders

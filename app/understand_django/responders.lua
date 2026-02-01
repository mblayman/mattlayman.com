local http = require("nibiru.http")
local render = require("nibiru.template").render

local pages = require("app.understand_django.pages")

local responders = {}

function responders.chapter(request, slug)
    local page = pages.get(slug)
    if page then
        local context = {
            page = page,
            pages = pages,
        }
        for k, v in pairs(page) do
            context[k] = v
        end
        return render("understand-django/chapter.html", context)
    else
        return http.not_found()
    end
end

return responders

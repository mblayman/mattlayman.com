local pages_module = require("app.pages")

return pages_module.load("pages/blog", { "slug", "title", "date" })

local markdown = require("nibiru.markdown")
local path = require("nibiru.path")

local pages = {}

local cached_sorted_pages = nil

-- Loads all markdown pages from the pages/blog directory.
-- Parses each file, validates frontmatter (slug, title, date required),
-- and stores them in the pages table indexed by slug.
local function load()
    local dir = "pages/blog"
    local files = path.files_from(dir)
    for _, file in ipairs(files) do
        if not file:match("%.md$") then
            error("Non-markdown file: " .. file)
        end

        local file_path = dir .. "/" .. file
        local f = io.open(file_path, "r")
        if not f then
            error("Could not open file: " .. file)
        end
        local content = f:read("*a")
        f:close()

        local parsed, err = markdown.parse(content)
        if err then
            error("Parse error for file " .. file .. ": " .. err)
        end
        if not parsed.frontmatter then
            error("No frontmatter found for file: " .. file)
        end

        local missing = {}
        if not parsed.frontmatter.slug then
            table.insert(missing, "slug")
        end
        if not parsed.frontmatter.title then
            table.insert(missing, "title")
        end
        if not parsed.frontmatter.date then
            table.insert(missing, "date")
        end

        if #missing > 0 then
            error(
                "Missing fields in frontmatter for file: "
                    .. file
                    .. ": "
                    .. table.concat(missing, ", ")
            )
        end

        parsed.filename = file
        -- Flatten frontmatter fields to the page level
        for key, value in pairs(parsed.frontmatter) do
            parsed[key] = value
        end
        local slug = parsed.slug
        if pages[slug] then
            error("Duplicate slug: " .. slug)
        end
        pages[slug] = parsed
    end

    -- Create cached sorted list by date descending
    local sorted = {}
    for _, page in pairs(pages) do
        table.insert(sorted, page)
    end
    table.sort(sorted, function(a, b)
        return a.date > b.date
    end)
    cached_sorted_pages = sorted
end

-- Retrieves a page by its slug from the loaded pages.
-- @param slug string: The slug of the page to retrieve.
-- @return The parsed page data or nil if not found.
local function get(slug)
    return pages[slug]
end

-- Retrieves all pages sorted by date in descending order.
-- @return The cached sorted list of pages.
local function list_by_date()
    return cached_sorted_pages
end

return {
    load = load,
    get = get,
    list_by_date = list_by_date,
}

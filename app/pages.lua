local markdown = require("nibiru.markdown")
local path = require("nibiru.path")

-- Loads all markdown pages from the specified directory.
-- Parses each file, validates frontmatter with required keys,
-- and returns a pages table with methods for accessing pages.
-- @param dir string: The relative path to the pages directory.
-- @param required_keys table: Table of required frontmatter keys.
-- @return pages table: Table containing loaded pages and access methods.
local function load(dir, required_keys)
    local pages = {}
    local cached_sorted_pages = nil

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
        for _, key in ipairs(required_keys) do
            if not parsed.frontmatter[key] then
                table.insert(missing, key)
            end
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

    -- Add methods to pages table
    pages.get = function(slug)
        return pages[slug]
    end

    pages.list_by_date = function()
        return cached_sorted_pages
    end

    return pages
end

return {
    load = load,
}
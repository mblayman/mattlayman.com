local Template = require("nibiru.template")

math.randomseed(os.time())

local colors = { "lime", "orange", "pink" }

local dark_accents = {
    lime = "oklch(64.8% 0.2 131.684)",
    orange = "oklch(70.5% 0.213 47.604)",
    pink = "oklch(52.5% 0.223 3.958)",
}

local light_accents = {
    lime = "oklch(53.2% 0.157 131.589)",
    orange = "oklch(64.6% 0.222 41.116)",
    pink = "oklch(45.9% 0.187 3.815)",
}

Template.register_function("accent_color", function(context, type)
    if not context.accent_color then
        context.accent_color = colors[math.random(1, #colors)]
    end

    if type == "dark" then
        return dark_accents[context.accent_color]
    end
    return light_accents[context.accent_color]
end)

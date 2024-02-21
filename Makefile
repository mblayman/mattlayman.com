.PHONY = tailwind css

local:
	heroku local

tailwind:
	cd themes/tailwind-site && npm run tailwind

css:
	cd themes/tailwind-site && npm run css

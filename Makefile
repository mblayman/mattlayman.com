.PHONY = tailwind css

new-local:
	air

local:
	heroku local

tailwind:
	cd themes/tailwind-site && npm run tailwind

css:
	cd themes/tailwind-site && npm run css

run:
	nibiru app.entry:app

deps:
	luarocks install --tree .rocks \
		https://github.com/mblayman/nibiru/raw/main/nibiru-dev-1.rockspec

image:
	docker build -t lua-app .

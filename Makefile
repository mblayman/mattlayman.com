.PHONY = tailwind css

local:
	heroku local

tailwind:
	cd themes/tailwind-site && npm run tailwind

css:
	cd themes/tailwind-site && npm run css

deps:
	luarocks install --tree .rocks \
		https://github.com/mblayman/nibiru/raw/main/nibiru-dev-1.rockspec

image:
	docker build -t lua-app .

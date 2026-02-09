local:
	air

deps:
	luarocks install --tree .rocks \
		https://github.com/mblayman/nibiru/raw/main/nibiru-dev-1.rockspec

image:
	docker build -t lua-app .

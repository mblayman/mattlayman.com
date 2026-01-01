FROM alpine:latest AS builder

RUN apk add --no-cache lua5.4 lua5.4-dev lua5.4-libs luarocks5.4 gcc musl-dev git

COPY . /srv
WORKDIR /srv

# Set environment variables for compilation
ENV CFLAGS="-I/usr/include/lua5.4"
ENV LDFLAGS="-L/usr/lib"

# Create symlink for liblua.so
RUN ln -s /usr/lib/liblua-5.4.so.0 /usr/lib/liblua.so

RUN luarocks-5.4 install --tree /srv/rocks \
    https://github.com/mblayman/nibiru/raw/main/nibiru-dev-1.rockspec

FROM alpine:latest

RUN apk add --no-cache lua5.4 lua5.4-libs

COPY --from=builder /srv /srv
WORKDIR /srv

CMD ["/srv/rocks/bin/nibiru", "run", "app.entry:app"]

from handroll.extensions.base import Extension


class ObnoxiousExtension(Extension):
    handle_pre_composition = True
    handle_frontmatter_loaded = True
    handle_post_composition = True

    def on_pre_composition(self, director):
        print 'Let\'s get this party started!'

    def on_frontmatter_loaded(self, source_file, frontmatter):
        print 'YO! Da front matter loaded.'

    def on_post_composition(self, director):
        print 'Peace out, homeslice!'

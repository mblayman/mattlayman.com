const purgecss = require('@fullhuman/postcss-purgecss')({
  content: [
    './layouts/**/*.html',
  ],

  // Overriding the default extractor because the default doesn't consider colon
  // and Tailwind makes heavy use of that as a class name.
  defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
})

module.exports = {
  plugins: [
    require('tailwindcss'),
    require('autoprefixer'),
    purgecss,
  ]
}

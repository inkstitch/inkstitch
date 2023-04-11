module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        useBuiltIns: 'usage', // adds specific imports for polyfills when they are used in each file.
        modules: false, // preserve ES modules.
        corejs: { version: 3, proposals: true }, // enable polyfilling of every proposal supported by core-js.
      },
    ],
  ],
  plugins: [
    '@babel/plugin-transform-runtime', // enables the re-use of Babel's injected helper code to save on codesize.
  ],
  exclude: [/core-js/],
}

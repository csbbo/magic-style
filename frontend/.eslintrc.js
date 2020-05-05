module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  'extends': [
    "plugin:vue/essential",
    "eslint:recommended"
  ],
  rules: {
    "no-console":process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    "no-unused-vars":0
  },
  parserOptions: {
    parser: "babel-eslint"
  }
}
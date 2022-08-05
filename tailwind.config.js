/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./website/templates/**/*.html",
    "./website/static/src/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
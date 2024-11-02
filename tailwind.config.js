/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
        './templates/**/*.html',
        './base/templates/**/*.html',
        './base/templates/components/**/*.html',
        './members/templates/**/*.html'
    ],
  },
  theme: {
    extend: {},
  },
  plugins: [],
}


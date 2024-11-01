/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
        './templates/**/*.html',
        './base/templates/**/*.html',
        './members/templates/**/*.html'
    ],
  },
  theme: {
    extend: {},
  },
  plugins: [],
}


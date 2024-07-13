/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/src/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        success: {
          200: '#d4edda',
          400: '#c3e6cb',
          700: '#155724',
        },
        error: {
          200: '#f8d7da',
          400: '#f5c6cb',
          700: '#721c24',
        },
        warning: {
          200: '#fff3cd',
          400: '#ffeeba',
          700: '#856404',
        },
        info: {
          200: '#d1ecf1',
          400: '#bee5eb',
          700: '#0c5460',
        },
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
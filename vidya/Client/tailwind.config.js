/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'theme-green': '#b9ff66',
        'theme-dark': '#191a23',
        'theme-light': '#f3f3f3',
      },
    },
  },
  plugins: [require('daisyui')],
}


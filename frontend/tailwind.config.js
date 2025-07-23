/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: 'class',  // enable class-based dark mode
  theme: {
    extend: {
      colors: {
        primary: "#1A73E8",        // "Monday blue" accent color
        'primary-dark': '#1662c4'  // darker shade for hover
      }
    }
  },
  plugins: []
}

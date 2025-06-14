/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    ],
  theme: {
    extend: {
      colors: {
        bgBipColor: "#d1d1d1",
        logoBipColor: "#003d87",
        navFont: "#0f233b",
      }
    },
  },
  plugins: [],
}


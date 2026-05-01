/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: '#1B2A4A',
        gold: '#C9A84C',
        'light-gold': '#E8D59E',
        'dark-navy': '#0F1A2F',
      },
      fontFamily: {
        arabic: ['Amiri', 'serif'],
        heading: ['Outfit', 'sans-serif'],
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#fdf9f0',
          100: '#faf0db',
          200: '#f5e0b3',
          300: '#edc97a',
          400: '#e5b24a',
          500: '#d49a2e',
          600: '#b87f24',
          700: '#96691f',
          800: '#7d571e',
          900: '#66471b',
          950: '#3b250d',
          DEFAULT: '#d49a2e',
          light: '#e5b24a',
        },
        dark: {
          50: '#f6f6f6',
          100: '#e7e7e7',
          200: '#d1d1d1',
          300: '#b0b0b0',
          400: '#888888',
          500: '#6d6d6d',
          600: '#5d5d5d',
          700: '#4f4f4f',
          800: '#454545',
          900: '#3d3d3d',
          950: '#0a0a0a',
          DEFAULT: '#2a2a2a',
        },
        primary: '#0a0a0a',
        secondary: '#141414',
        tertiary: '#1a1a1a',
        card: '#1f1f1f',
        muted: '#888888',
      },
    },
  },
  plugins: [],
}

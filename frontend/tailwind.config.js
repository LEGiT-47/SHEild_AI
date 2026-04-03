/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        sheild: {
          dark: "#0a0a0a",
          paper: "#e8e0d0",
          red: "#c0392b",
          green: "#2ecc71",
          cyan: "#00cc88",
          mid: "#3d3d3d",
          card: "#141414",
        },
      },
      fontFamily: {
        display: ["Playfair Display", "serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      keyframes: {
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        blink: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.2" },
        },
      },
      animation: {
        scanline: "scanline 8s linear infinite",
        blink: "blink 1.2s steps(2, end) infinite",
      },
    },
  },
  plugins: [],
};

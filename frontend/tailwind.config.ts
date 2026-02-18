import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                foreground: "var(--foreground)",
                uae: {
                    gold: "#bfa588",
                    "gold-hover": "#a88e70",
                    green: "#007a33",
                    black: "#000000",
                    white: "#ffffff",
                    gray: "#f8f9fa",
                    "dark-gray": "#343a40",
                }
            },
            fontFamily: {
                sans: ['var(--font-inter)', 'sans-serif'],
                arabic: ['var(--font-tajawal)', 'sans-serif'],
            },
        },
    },
    plugins: [],
};
export default config;

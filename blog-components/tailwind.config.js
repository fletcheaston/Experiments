"use strict"
/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{js,ts,jsx,tsx,mdx,css}"],
    theme: {
        extend: {
            colors: {
                primary: "var(--md-primary-fg-color)",
                "primary-hover": "var(--md-primary-fg-color--dark)",
                secondary: "var(--md-accent-fg-color)",
            },
        },
    },
    darkMode: ["class"],
    plugins: [require("@tailwindcss/forms")],
    prefix: "tw-",
}

"use strict"
/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{js,ts,jsx,tsx,mdx}", "./src/**/*.css"],
    theme: {
        extend: {
            colors: {
                primary: "var(--md-primary-fg-color)",
                "primary-hover": "var(--md-primary-fg-color--dark)",
            },
        },
    },
    darkMode: ["class"],
    plugins: [require("@tailwindcss/forms")],
    prefix: "tw-",
}

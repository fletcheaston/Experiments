/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/styles/**/*.css",
    ],
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

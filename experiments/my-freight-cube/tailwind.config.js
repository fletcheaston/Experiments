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
                primary: "rgb(var(--primary-rgb))",
                "primary-hover": "rgb(var(--primary-hover-rgb))",
            },
        },
    },
    darkMode: ["class"],
    plugins: [require("@tailwindcss/forms")],
}

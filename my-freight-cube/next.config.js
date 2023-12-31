/** @type {import('next').NextConfig} */
const nextConfig = {
    basePath: "/my-freight-cube",
    experimental: {
        typedRoutes: true,
    },
    output: "export",
    distDir: "build",
    images: {
        loader: "custom",
        loaderFile: "./image-loader.ts",
    },
}

module.exports = nextConfig

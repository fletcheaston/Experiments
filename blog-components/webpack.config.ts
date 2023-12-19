import MiniCssExtractPlugin from "mini-css-extract-plugin"
import path from "path"
import { Configuration } from "webpack"

const config: Configuration = {
    mode: "production",
    entry: ["./src/exports/index.ts"],
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: [
                    {
                        loader: "ts-loader",
                        options: {
                            configFile: "webpack.tsconfig.json",
                        },
                    },
                ],
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    { loader: MiniCssExtractPlugin.loader },
                    "css-loader",
                    "postcss-loader",
                ],
                sideEffects: true,
            },
        ],
    },
    resolve: {
        extensions: [".js", ".jsx", ".ts", ".tsx"],
        alias: {
            "@components": path.resolve(__dirname, "src/components/"),
            "@styles": path.resolve(__dirname, "src/styles/"),
            "@src": path.resolve(__dirname, "src/"),
        },
    },
    output: {
        filename: "blog-components.js",
        path: path.resolve(__dirname, "dist"),
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "blog-components.css",
        }),
    ],
    ignoreWarnings: [
        {
            module: /.\/src\/styles\/globals.css/,
        },
    ],
}

export default config

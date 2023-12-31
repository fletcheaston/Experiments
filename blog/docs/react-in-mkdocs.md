---
title: React in MkDocs
---


Super simple example!
There's a button to reset the number of clicks, and a button that increments clicks.

And because it's a well-defined React component, we can have any number of these on the page without conflicts.

<div class="grid">
<div data-component="clicked-button"></div>

<div data-component="clicked-button"></div>
</div>

## Motivation

- I wanted to build some highly-interactive visualizations for my [Advent of Code 2023 problems](advent-of-code/2023/index.md)
    - In particular, days [6](advent-of-code/2023/day-6.md) and [10](advent-of-code/2023/day-10.md) looked like a ton of fun to visualize and play with
- I didn't want to build an entirely new website *just* for visualizations

## Overview

MkDocs and Material for MkDocs are **amazing** tools to build responsive, accessible, great looking static sites.

By design, these sites lean towards more "static" content than "dynamic" content.
Sure, you can use components like [adminitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/), [tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/), and [tables](https://squidfunk.github.io/mkdocs-material/reference/data-tables/), which all offer some level of interactivity, but the lack of dynamic content felt very limiting.

## Constraints

- I'm using TypeScript, Tailwindcss, and whatever other libraries I feel like
- I need fast feedback cycles for developing the React components
- I need a dead-simple integration for using those components in MkDocs

Pretty simple, right?
These constraints pushed me in (what felt like) an obvious direction.

### Ideal Workflow

- Write some React components in a separate project
- Transpile those React components to a JS script
- Include that JS script with MkDocs
- Use a tagged `div` to load each React component

## Tooling/Configuration

I'm very comfortable setting up and building Next.js sites.
That Next.js site won't be published or deployed anywhere, it won't even be built.
I'm just using it for local development and fast feedback cycles while I'm building out my React components.
It ships with sensible defaults and configurations and saves me a lot of time getting the project stood up.

I could've used Vite, CRA, or any other tool here.
But I'm comfortable with Next.js (although it does [one really annoying thing](#webpacktsconfigjson)).

### Next.js

No custom configuration, the default configuration from `npx create-next-app@latest` works great.
Every component is marked with the `"use client"` directive.

### Tailwind


#### `tailwind.config.ts`

Note the usage of `--md-primary-fg-color` and `--md-primary-fg-color--dark`.
These two CSS variables are used in Material for MkDocs, and automatically update based on whether you're in light-mode or dark-mode.
You can see this by viewing the example above and toggling between modes.

This pushes the color configuration down to MkDocs so everything is nice and synced.

Also note the usage of the `tw-` prefix for all Tailwind classes.
I was a little nervous about Tailwind accidentially overwriting classes used elsewhere, so I figured that prefixing our classes couldn't hurt.

```typescript
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
```

#### `src/styles/global.css`

Basic Tailwind CSS integration file with a few custom classes.

Note that I included the `--md-primary-fg-color` and `--md-primary-fg-color--dark` CSS variables here.
These will obviously be different when the CSS is imported into MkDocs, but those variables are required for local development in Next.js.

It's very trendy to hate the [`@apply` directive](https://tailwindcss.com/docs/reusing-styles#extracting-classes-with-apply), but I find it very useful for `btn` classes.
It gives me consistent styling for my buttons with minimal effort, but still enables me to overwrite that styling if needed.

I noted this at the top of the file, but it's important to not include `@tailwind base` in this file.
`@tailwind base` overwrites the default styling of buttons, headers, and more in the browser so you can give those elements custom styles very easily (aka without the `!important` tag).
Material for MkDocs does a great job handling the styling for most of those elements.

This does mean that I need to include some classes that I wouldn't normally need to include.
For example, the `tw-btn` class has `tw-cursor-pointer`.
Without this, the cursor wouldn't change to a pointer when hovering over a button.
The same reason applies for `tw-cursor-auto` on `tw-btn:disabled`.

I do have `@tailwind base` in a separate CSS file when I'm doing local development with Next.js, it's just not included by Webpack.

```css
/* DO NOT use `@tailwind base` here, it'll overwrite far too many base styles */
@tailwind components;

/*****************************************************************************/
/* Global vars */
:root {
    --md-primary-fg-color: #7e56c2;
    --md-primary-fg-color--dark: #673ab6;
}

/*****************************************************************************/
/* Buttons */
@layer components {
    .tw-btn {
        @apply tw-cursor-pointer tw-rounded tw-px-4 tw-py-1 tw-text-center tw-transition-all hover:tw-bg-slate-100;
    }

    .tw-btn-lg {
        @apply tw-py-2 tw-text-xl;
    }

    .tw-btn-sm {
        @apply tw-px-2;
    }

    .tw-btn-primary {
        @apply tw-bg-primary tw-text-white hover:tw-bg-primary-hover;
    }

    .tw-btn-primary-text {
        @apply tw-bg-transparent tw-text-primary hover:tw-bg-primary hover:tw-text-white;
    }

    .tw-btn-primary-outline {
        @apply tw-border-[1px] tw-border-primary tw-bg-transparent tw-text-primary hover:tw-bg-primary hover:tw-text-white;
    }

    .tw-btn:disabled {
        @apply tw-cursor-auto tw-opacity-60;
    }
}

@tailwind utilities;
```

#### `postcss.config.js`

Nothing special here.

```javascript
module.exports = {
    plugins: {
        "postcss-import": {},
        "tailwindcss/nesting": {},
        tailwindcss: {},
        autoprefixer: {},
    },
}
```

### TypeScript

#### `tsconfig.json`

Most of these settings match what Next.js provides out of the box.

Some personal preferences in my TypeScript projects:

- I love custom paths, I hate relative imports (unless it's in the same directory, then it's acceptable)
- I use `spine-case` file/module names
- I always use strict mode. Why even use TypeScript if you don't care about the errors/warnings it gives?

```json
{
    "compilerOptions": {
        "target": "es6",
        "lib": ["dom", "dom.iterable", "es6"],
        "allowJs": true,
        "skipLibCheck": true,
        "strict": true,
        "forceConsistentCasingInFileNames": true,
        "noEmit": false,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "node",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "preserve",
        "incremental": true,
        "plugins": [
            {
                "name": "next"
            }
        ],
        "paths": {
            "@components/*": ["./src/components/*"],
            "@styles/*": ["./src/styles/*"],
            "@src/*": ["./src/*"]
        }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
}
```

### Webpack

#### `webpack.tsconfig.json`

I have a slightly different TypeScript configuration for my Webpack builds.

Why?
Because Webpack needs `"jsx": "react-jsx"` to work, and Next.js needs `"jsx": "preserve"` to work.

This was actually super annoying to figure out:

1. I set `"jsx": "react-jsx"` in `tsconfig.json`
2. I (successfully) ran my Webpack build step
3. I ran my Next.js server for local dev
4. I ran my Webpack build step again and it would fail

What I didn't see was this message in my terminal:

!!! warning

    We detected TypeScript in your project and reconfigured your tsconfig.json file for you. Strict-mode is set to false by default.

    The following mandatory changes were made to your tsconfig.json:

   	- jsx was set to preserve (next.js implements its own optimized jsx transform)

When you run `npm run dev` (`next dev`), Next.js will *automatically* update your `tsconfig.json` file to change `"jsx"` to `"preserve"`.
AFAIK, you cannot alter this behavior in any way.

```json
{
    "compilerOptions": {
        "outDir": "./dist/",
        "target": "es6",
        "lib": ["dom", "dom.iterable", "es6"],
        "allowJs": true,
        "skipLibCheck": true,
        "strict": true,
        "forceConsistentCasingInFileNames": true,
        "noEmit": false,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "node",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "react-jsx",
        "incremental": true,
        "plugins": [
            {
                "name": "next"
            }
        ],
        "paths": {
            "@components/*": ["./src/components/*"],
            "@styles/*": ["./src/styles/*"],
            "@src/*": ["./src/*"]
        }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
}
```

#### `webpack.config.ts`

I have almost no experience with Webpack (thank you Next.js ❤️), so I may be doing something silly/dumb/bad here ¯\\\_(ツ)_/¯.

But it does work!

Some things to note:

- I'm using the `webpack.tsconfig.json` file for my `ts-loader` step (see [above](#webpacktsconfigjson))
- I'm using [MiniCssExtractPlugin](https://www.npmjs.com/package/mini-css-extract-plugin) to pull out all styles/classes into a single CSS file
- There's a warning about `./src/styles/global.css` not having a default export, so I'm ignoring that warning

```typescript
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
                use: ["style-loader", { loader: MiniCssExtractPlugin.loader }, "css-loader", "postcss-loader"],
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
```

## Workflow

1. Run `npm run dev` to start my local Next.js server
2. Go to `http://localhost:3000/` to view all of my components
3. Work on some component in the `/src/components/` directory, super fast feedback cycles thanks to Next.js
4. Create an export file in the `/src/exports/` directory, mapping a `data-component` tag to my React component
5. Add the initialized for that component to the `/src/exports/index.ts` file so it's picked up by the global initialized
6. Run `npm run build` to run my Webpack build
7. Open the `dist` directory and copy the `blog-components.css` and `blog-components.js` files into `/docs/extras/` in my blog project
8. Render each component with a tagged `div`
    - The example at the top of the page uses `<div data-component="clicked-button"></div>`

### Clicked Button - JSX

```jsx
"use client"

import React, { useState } from "react"

export function ClickedButton() {
    /**************************************************************************/
    /* State */
    const [clicks, setClicks] = useState(0)

    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-gap-4">
            <button
                className="tw-btn tw-btn-primary"
                onClick={() => {
                    setClicks(0)
                }}
            >
                Reset Clicks
            </button>

            <button
                className="tw-btn tw-btn-primary"
                onClick={() => {
                    setClicks((prevState) => prevState + 1)
                }}
            >
                Clicked {clicks} time{clicks === 1 ? "" : "s"}
            </button>
        </div>
    )
}
```

### Clicked Button - Export

```jsx
"use strict"

import React from "react"
import { createRoot } from "react-dom/client"

import { ClickedButton } from "@components/clicked-button"

export function initialize() {
    document.querySelectorAll("[data-component='clicked-button']").forEach((element) => {
        const root = createRoot(element)
        root.render(<ClickedButton />)
    })
}
```

### `index.ts` - Export

Note that our `initializeBlogComponents` function is exposed on the `window` object.

```typescript
import "@styles/globals.css"

import { initialize as initializeClickedButtons } from "./clicked-button"

function initializeBlogComponents() {
    initializeClickedButtons()
}

declare global {
    interface Window {
        initializeBlogComponents: () => void
    }
}

window.initializeBlogComponents = initializeBlogComponents
```

### MkDocs Config

There is a lot more to this file, but this is whats required to get our React components working.

```yaml
theme:
    custom_dir: overrides

extra_css:
    - extras/blog-components.css

extra_javascript:
    - extras/blog-components.js
```

### `main.html` - MkDocs

Used to [override the base HTML template](https://squidfunk.github.io/mkdocs-material/customization/#overriding-blocks).
We use that exposed `initializeBlogComponents` function here.

`document$.subscribe` comes from [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/customization/#additional-javascript).
Every time we load a page (whether thats a full-page load or an SPA-like load), we re-initialize all blog components.

```html
{% extends "base.html" %}

{% block scripts %}
    <!-- Add scripts that need to run before here -->

    {{ super() }}

    <!-- Add scripts that need to run afterwards here -->
    <script>
        document$.subscribe(function() {
            window.initializeBlogComponents()
        })
    </script>
{% endblock %}
```

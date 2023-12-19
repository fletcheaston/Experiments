import { Inter } from "next/font/google"
import React from "react"

import ClientOnly from "@src/client-only"

import "@styles/base.css"
import "@styles/globals.css"

const inter = Inter({ subsets: ["latin"] })
export const metadata = {
    title: "Blog Components",
}
export default function RootLayout(props) {
    /**************************************************************************/
    /* Render */
    return (
        <html lang="en">
            <body className={inter.className}>
                <ClientOnly>{props.children}</ClientOnly>
            </body>
        </html>
    )
}

import { cn } from "@utils"
import classNames from "classnames"
import { Inter } from "next/font/google"
import Image from "next/image"
import Link from "next/link"
import React from "react"

import { Button } from "@components/ui/button"

import GitHub from "@images/github-mark.svg"

import "@styles/globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
    title: "Flotion",
}

export default function RootLayout({ children }: { children: React.JSX.Element }) {
    /**************************************************************************/
    /* Render */
    return (
        <html lang="en">
            <body className={cn(classNames(inter.className), "relative")}>
                <nav className="sticky top-0 z-50 flex items-center gap-x-2 border-b-[1px] border-b-slate-300 bg-background px-3 py-2">
                    <Button
                        asChild
                        variant="link"
                        className="px-0 text-3xl"
                    >
                        <Link
                            href="/"
                            className="inline-flex flex-shrink-0 items-center gap-x-2"
                        >
                            📝 Flotion
                        </Link>
                    </Button>

                    <div className="flex-grow" />

                    <Button
                        asChild
                        variant="link"
                        className="text-xl"
                    >
                        <Link href="/documents">Documents</Link>
                    </Button>

                    <Button
                        asChild
                        variant="link"
                        className="text-xl"
                    >
                        <Link href="/documents/new">New</Link>
                    </Button>
                </nav>

                <main>{children}</main>

                <footer className="flex border-t-2 border-slate-600 px-2">
                    <Link
                        href="https://github.com/fletcheaston"
                        target="_blank"
                        className="flex items-center gap-x-2"
                    >
                        <Image
                            src={GitHub}
                            height={24}
                            alt="GitHub logo"
                            className="flex-shrink-0"
                        />

                        <span className="text-xl">GitHub</span>
                    </Link>
                </footer>
            </body>
        </html>
    )
}

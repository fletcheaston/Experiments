import { Dropdown } from "@/components/dropdown"
import { ChevronDown } from "@icons/chevron-down"
import { Gear } from "@icons/gear"
import { Inter } from "next/font/google"
import Image from "next/image"
import Link from "next/link"
import React from "react"

import "@styles/globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
    title: "MyFreightCube",
    description: "Sponsored by 4WL Consulting.",
}

export default function RootLayout({ children }: { children: React.JSX.Element }) {
    return (
        <html
            lang="en"
            className="dark"
        >
            <body className={inter.className}>
                <nav className="flex items-center gap-x-2 px-3">
                    <Link href="/">
                        <Image
                            src="/logo-large.svg"
                            width={215}
                            height={50}
                            alt="MyFreightCube logo"
                            className="flex-shrink-0"
                        />
                    </Link>

                    <div className="flex-grow" />

                    <Dropdown
                        title={
                            <div className="flex flex-shrink-0 gap-x-2">
                                Calculators{" "}
                                <ChevronDown
                                    height={30}
                                    width={20}
                                    className="text-inherit"
                                />
                            </div>
                        }
                        links={[
                            {
                                href: "/calculators/air-freight-dim-weight",
                                children: "Air Freight Dim Weight",
                            },
                            {
                                href: "/calculators/parcel-dim-weight",
                                children: "Parcel Dim Weight",
                            },
                            {
                                href: "/calculators/ltl-density",
                                children: "LTL Density",
                            },
                            {
                                href: "/calculators/lineal-foot",
                                children: "Lineal Foot",
                            },
                        ]}
                    />

                    <Link
                        href="/how-it-works"
                        className="btn btn-lg btn-primary-outline"
                    >
                        How It Works
                    </Link>

                    <Link
                        href="/settings"
                        className="btn btn-primary-outline p-2"
                    >
                        <Gear
                            height={28}
                            width={28}
                            className="text-inherit"
                        />
                    </Link>
                </nav>

                <main>{children}</main>
            </body>
        </html>
    )
}

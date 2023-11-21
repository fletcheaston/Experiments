"use client"

import { useLiveQuery } from "dexie-react-hooks"
import Link from "next/link"
import React, { useEffect, useState } from "react"

import { Carrier, database } from "@components/database"
import { Divider } from "@components/divider"
import { NumberInput } from "@components/input"
import { Table } from "@components/table"

const predefinedCarriers: Array<Carrier> = [
    {
        id: crypto.randomUUID(),
        created: new Date(),
        default: null,
        name: "FedEx",
        dimDivisor: 139.0,
    },
    {
        id: crypto.randomUUID(),
        created: new Date(),
        default: null,
        name: "UPS",
        dimDivisor: 139.0,
    },
    {
        id: crypto.randomUUID(),
        created: new Date(),
        default: null,
        name: "USPS",
        dimDivisor: 139.0,
    },
]

export default function Page() {
    /**************************************************************************/
    /* State */
    const [inchLength, setInchLength] = useState(0)
    const [inchWidth, setInchWidth] = useState(0)
    const [inchHeight, setInchHeight] = useState(0)
    const [pounds, setPounds] = useState(0)

    const rawCarriers = useLiveQuery(() => database.carriers.orderBy("created").toArray())
    const [carriers, setCarriers] = useState(rawCarriers)

    const volume = inchLength * inchWidth * inchHeight

    const allNumbersValid = !!inchLength && !!inchWidth && !!inchHeight && !!pounds

    /**************************************************************************/
    /* Effects */
    // Only refresh the carrier list when it's loaded
    useEffect(() => {
        if (!rawCarriers) {
            return
        }

        setCarriers([...predefinedCarriers, ...rawCarriers])
    }, [rawCarriers])

    /**************************************************************************/
    /* Render */
    return (
        <div className="flex flex-col justify-between gap-8 px-16 py-8 md:flex-row">
            <div>
                <h1 className="text-5xl font-semibold">Parcel Dim Weight Calculator</h1>

                <p className="mt-2">
                    Choose the appropriate carriers. If you don&apos;t see the carrier you need,{" "}
                    <Link
                        href="/settings"
                        className="text-primary"
                    >
                        add a new preset to your account
                    </Link>
                    .
                </p>

                <div className="mt-8 flex flex-wrap gap-4">
                    <NumberInput
                        className="w-full flex-shrink-0 md:w-[120px]"
                        label="Length (in)"
                        step={0.01}
                        value={inchLength}
                        setValue={setInchLength}
                    />

                    <NumberInput
                        className="w-full flex-shrink-0 md:w-[120px]"
                        label="Width (in)"
                        step={0.01}
                        value={inchWidth}
                        setValue={setInchWidth}
                    />

                    <NumberInput
                        className="w-full flex-shrink-0 md:w-[120px]"
                        label="Height (in)"
                        step={0.01}
                        value={inchHeight}
                        setValue={setInchHeight}
                    />

                    <NumberInput
                        className="w-full flex-shrink-0 md:w-[120px]"
                        label="Weight (lbs)"
                        step={0.01}
                        value={pounds}
                        setValue={setPounds}
                    />
                </div>

                <div className="mt-8 w-fit rounded border-[1px] border-slate-300 p-4">
                    <h2 className="whitespace-nowrap text-xl font-semibold">Results</h2>

                    <Divider className="mb-2" />

                    <Table
                        columns={[
                            {
                                title: "Name",
                                width: "150px",
                                align: "left",
                                renderer: (row) => {
                                    return row.name
                                },
                            },
                            {
                                title: "Dim Divisor",
                                width: "110px",
                                align: "right",
                                renderer: (row) => {
                                    return row.dimDivisor
                                },
                            },
                            {
                                title: "Billable Weight",
                                width: "140px",
                                align: "right",
                                renderer: (row) => {
                                    if (allNumbersValid) {
                                        const dimensionalWeight = volume / row.dimDivisor
                                        return `${Math.round(Math.max(dimensionalWeight, pounds)).toLocaleString()} lbs`
                                    }

                                    return "N/A"
                                },
                            },
                        ]}
                        rows={carriers}
                    />
                </div>
            </div>
        </div>
    )
}

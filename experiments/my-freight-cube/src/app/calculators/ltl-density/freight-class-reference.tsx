import React from "react"

import { Divider } from "@components/divider"
import { Table } from "@components/table"

export interface FreightClass {
    min?: number
    max?: number
    freightClass: number
}

export const freightClassReference: Array<FreightClass> = [
    {
        max: 1,
        freightClass: 400,
    },
    {
        min: 1,
        max: 2,
        freightClass: 300,
    },
    {
        min: 2,
        max: 4,
        freightClass: 250,
    },
    {
        min: 4,
        max: 6,
        freightClass: 175,
    },
    {
        min: 6,
        max: 8,
        freightClass: 125,
    },
    {
        min: 8,
        max: 10,
        freightClass: 100,
    },
    {
        min: 10,
        max: 12,
        freightClass: 92.5,
    },
    {
        min: 12,
        max: 15,
        freightClass: 85,
    },
    {
        min: 15,
        max: 22.5,
        freightClass: 70,
    },
    {
        min: 22.5,
        max: 30,
        freightClass: 65,
    },
    {
        min: 30,
        max: 35,
        freightClass: 60,
    },
    {
        min: 35,
        max: 50,
        freightClass: 55,
    },
    {
        min: 50,
        freightClass: 50,
    },
]

export function FreightClassReference() {
    return (
        <div className="flex-shrink border-[1px] border-slate-300 px-4 pb-1 pt-4">
            <h2 className="whitespace-nowrap text-xl font-semibold">Freight Class Reference</h2>

            <Divider className="mb-2" />

            <Table
                columns={[
                    {
                        title: "Density (lbs / ft³)",
                        width: "180px",
                        align: "left",
                        renderer: (row) => row.id,
                    },
                    {
                        title: "Class",
                        width: "80px",
                        align: "right",
                        renderer: (row) => row.freightClass,
                    },
                ]}
                rows={freightClassReference.map((freightClass) => {
                    let id = `${freightClass.min} – ${freightClass.max} lbs.`

                    if (!freightClass.min) {
                        id = `Under ${freightClass.max} lbs.`
                    }

                    if (!freightClass.max) {
                        id = `Over ${freightClass.min} lbs.`
                    }

                    return {
                        ...freightClass,
                        id,
                    }
                })}
                rowClassName={() => {
                    return "border-b-[1px] border-slate-300 last-of-type:border-0 h-10"
                }}
            />
        </div>
    )
}

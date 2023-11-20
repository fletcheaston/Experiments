"use client"

import React, { useState } from "react"

import { FreightClassReference } from "./freight-class-reference"
import { Item, ItemList } from "./items"

export default function Page() {
    /**************************************************************************/
    /* State */
    const [items, setItems] = useState<Array<Item>>([])

    /**************************************************************************/
    /* Render */
    return (
        <div className="flex flex-col justify-between gap-8 px-16 py-8 md:flex-row">
            <div>
                <h1 className="text-5xl font-semibold">LTL Density Calculator</h1>

                <p className="mt-2">
                    Enter the length, width, height, and weight for each item. You can add as many items as you need.
                </p>

                <ItemList
                    items={items}
                    updateItems={setItems}
                />

                <div className="mt-4 flex justify-between">
                    <button
                        className="btn btn-primary-outline"
                        onClick={() => {
                            setItems((prevState) => {
                                return [
                                    ...prevState,
                                    {
                                        id: crypto.randomUUID(),
                                        name: "Item",
                                        inchLength: 0,
                                        inchWidth: 0,
                                        inchHeight: 0,
                                        poundsPerUnit: 0,
                                    },
                                ]
                            })
                        }}
                    >
                        Add Item
                    </button>

                    <button
                        className="btn btn-primary-outline"
                        onClick={() => {
                            setItems([
                                {
                                    id: crypto.randomUUID(),
                                    name: "Item",
                                    inchLength: 0,
                                    inchWidth: 0,
                                    inchHeight: 0,
                                    poundsPerUnit: 0,
                                },
                            ])
                        }}
                    >
                        Clear
                    </button>
                </div>
            </div>

            <div className="flex-shrink-0">
                <FreightClassReference />
            </div>
        </div>
    )
}

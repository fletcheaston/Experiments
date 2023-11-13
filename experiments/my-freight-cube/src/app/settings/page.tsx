import React from "react"

import { AddCarrier, CarriersList } from "./carriers"

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <div className="px-16">
            <h1 className="mt-8 text-5xl font-semibold">Settings</h1>

            <div className="flex items-end justify-between">
                <h2 className="mt-6 text-3xl font-semibold">My Carriers</h2>

                <AddCarrier />
            </div>

            <CarriersList />

            <h2 className="mt-6 text-3xl font-semibold">My Equipment</h2>

            <h2 className="mt-6 text-3xl font-semibold">My Saved Results</h2>
        </div>
    )
}

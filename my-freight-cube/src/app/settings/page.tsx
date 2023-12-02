import React from "react"

import { Carriers } from "./carriers"
import { Equipment } from "./equipment"

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <div className="px-16">
            <h1 className="mt-8 text-5xl font-semibold">Settings</h1>

            <div className="mt-6 flex flex-wrap gap-x-6 gap-y-12">
                <Carriers />

                <Equipment />
            </div>

            <div className="max-w-[500px]">
                <h2 className="mt-6 text-3xl font-semibold">My Saved Results</h2>
            </div>
        </div>
    )
}

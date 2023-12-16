"use client"

import React, { useState } from "react"

import { Loading } from "@components/loading"

export function LoadingButton() {
    /**************************************************************************/
    /* State */
    const [loading, setLoading] = useState(false)

    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-gap-x-4">
            <div>
                <button
                    className="tw-btn tw-btn-primary"
                    onClick={() => {
                        setLoading(!loading)
                    }}
                >
                    Switch Loading
                </button>
            </div>

            <Loading on={loading}>
                <div>{loading ? "Loading" : "Loaded"}</div>
            </Loading>
        </div>
    )
}

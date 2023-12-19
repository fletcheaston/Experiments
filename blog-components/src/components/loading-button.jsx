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
        <Loading on={loading}>
            <button
                className="tw-btn tw-btn-primary"
                onClick={() => {
                    setLoading((prevState) => !prevState)
                }}
            >
                Toggle Loading
            </button>
        </Loading>
    )
}

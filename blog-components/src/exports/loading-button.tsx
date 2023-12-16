"use strict"

import React from "react"
import { createRoot } from "react-dom/client"

import { LoadingButton } from "@components/loading-button"

export function initializeLoadingButtons() {
    document.querySelectorAll("[data-component='loading-button']").forEach((element) => {
        const root = createRoot(element)
        root.render(<LoadingButton />)
    })
}

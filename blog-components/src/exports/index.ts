import "@styles/globals.css"

import { initializeLoadingButtons } from "./loading-button"

function initializeBlogComponents() {
    initializeLoadingButtons()
}

declare global {
    interface Window {
        initializeBlogComponents: () => void
    }
}

window.initializeBlogComponents = initializeBlogComponents

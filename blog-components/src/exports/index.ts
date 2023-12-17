import "@styles/globals.css"

import { initialize as initializeClickedButtons } from "./clicked-button"
import { initialize as initializeLoadingButtons } from "./loading-button"

function initializeBlogComponents() {
    initializeLoadingButtons()
    initializeClickedButtons()
}

declare global {
    interface Window {
        initializeBlogComponents: () => void
    }
}

window.initializeBlogComponents = initializeBlogComponents

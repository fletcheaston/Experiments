import "@styles/globals.css";
import { initialize as initializeClickedButtons } from "./clicked-button";
import { initialize as initializeLoadingButtons } from "./loading-button";
function initializeBlogComponents() {
    initializeLoadingButtons();
    initializeClickedButtons();
}
window.initializeBlogComponents = initializeBlogComponents;

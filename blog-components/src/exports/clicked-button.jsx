"use strict";
import React from "react";
import { createRoot } from "react-dom/client";
import { ClickedButton } from "@components/clicked-button";
export function initialize() {
    document.querySelectorAll("[data-component='clicked-button']").forEach((element) => {
        const root = createRoot(element);
        root.render(<ClickedButton />);
    });
}

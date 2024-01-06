"use client"

import { useState } from "react"
import { createEditor } from "slate"
import { Editable, Slate, withReact } from "slate-react"

import { renderElement } from "@components/slate/custom-elements/render"
import { renderLeaf } from "@components/slate/custom-leaves/render"
import { CustomElement } from "@components/slate/types"

const initialValue: Array<CustomElement> = [
    {
        type: "header",
        level: 1,
        children: [{ type: "plain", text: "H1 Header" }],
    },
    {
        type: "header",
        level: 2,
        children: [{ type: "plain", text: "Level 2 Header" }],
    },
    {
        type: "header",
        level: 3,
        children: [{ type: "plain", text: "Level 3 Header" }],
    },
    {
        type: "paragraph",
        children: [
            { type: "formatted", text: "A line ", bold: true },
            { type: "formatted", text: "of text ", italics: true },
            { type: "formatted", text: "in a ", strikethrough: true },
            { type: "formatted", text: "paragraph.", bold: true, italics: true, strikethrough: true },
        ],
    },
    {
        type: "code",
        language: "",
        children: [{ type: "plain", text: "Some code goes here" }],
    },
]

export function CustomEditor() {
    /**************************************************************************/
    /* State */
    const [editor] = useState(() => withReact(createEditor()))

    /**************************************************************************/
    /* Render */
    return (
        <Slate
            editor={editor}
            initialValue={initialValue}
            onChange={(e) => {
                console.log(e)
            }}
        >
            <Editable
                renderElement={renderElement}
                renderLeaf={renderLeaf}
                className="h-full rounded bg-slate-100 p-1"
            />
        </Slate>
    )
}

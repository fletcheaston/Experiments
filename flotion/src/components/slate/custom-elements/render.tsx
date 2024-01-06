import React from "react"
import { RenderElementProps } from "slate-react"

import { Code } from "@components/slate/custom-elements/code"
import { Header } from "@components/slate/custom-elements/header"
import { Paragraph } from "@components/slate/custom-elements/paragraph"

const elementTypeToRenderer = {
    header: Header,
    paragraph: Paragraph,
    list: (props) => <></>,
    code: Code,
    blockquote: (props) => <></>,
    divider: (props) => <></>,
} satisfies Record<RenderElementProps["element"]["type"], (props: RenderElementProps) => React.JSX.Element>

export function renderElement(props: RenderElementProps) {
    return elementTypeToRenderer[props.element.type](props)
}

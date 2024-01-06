import React from "react"
import { RenderLeafProps } from "slate-react"

import { Code } from "@components/slate/custom-leaves/code"
import { Formatted } from "@components/slate/custom-leaves/formatted"
import { Plain } from "@components/slate/custom-leaves/plain"

const leafTypeToRenderer = {
    plain: Plain,
    code: Code,
    formatted: Formatted,
    link: (props) => <></>,
    image: (props) => <></>,
} satisfies Record<RenderLeafProps["leaf"]["type"], (props: RenderLeafProps) => React.JSX.Element>

export function renderLeaf(props: RenderLeafProps) {
    return leafTypeToRenderer[props.leaf.type](props)
}

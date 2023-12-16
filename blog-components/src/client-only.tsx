import dynamic from "next/dynamic"
import React from "react"

const ClientOnly = (props: { children: React.ReactNode }) => props.children

export default dynamic(() => Promise.resolve(ClientOnly), {
    ssr: false,
})

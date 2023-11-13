"use client"

import { useId } from "react"

export function TextInput(props: {
    label: string
    placeholder: string
    required?: boolean
    value: string
    setValue: (value: string) => void
}) {
    /**************************************************************************/
    /* Render */
    const id = `input-${useId()}`

    /**************************************************************************/
    /* Render */
    return (
        <div className="relative">
            <label
                htmlFor={id}
                className="absolute -top-2 left-1.5 bg-white px-0.5 text-sm font-medium leading-4"
            >
                {props.label}
            </label>

            <input
                id={id}
                name={props.label}
                type="text"
                className="mt-2 block w-full rounded-md border-0 px-3 py-1.5 ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-primary"
                placeholder={props.placeholder}
                value={props.value}
                onChange={(event) => {
                    props.setValue(event.target.value)
                }}
                required={props.required}
            />
        </div>
    )
}

export function NumberInput(props: {
    label: string
    placeholder: number
    step: number
    min?: number
    max?: number
    required?: boolean
    value: number
    setValue: (value: number) => void
}) {
    /**************************************************************************/
    /* Render */
    const id = `input-${useId()}`

    /**************************************************************************/
    /* Render */
    return (
        <div className="relative">
            <label
                htmlFor={id}
                className="absolute -top-2 left-1.5 bg-white px-0.5 text-sm font-medium leading-4"
            >
                {props.label}
            </label>

            <input
                id={id}
                name={props.label}
                type="number"
                className="mt-2 block w-full rounded-md border-0 px-3 py-1.5 ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-primary"
                placeholder={props.placeholder.toString()}
                step={props.step}
                min={props.min}
                max={props.max}
                value={props.value}
                onChange={(event) => {
                    props.setValue(event.target.valueAsNumber)
                }}
                required={props.required}
            />
        </div>
    )
}

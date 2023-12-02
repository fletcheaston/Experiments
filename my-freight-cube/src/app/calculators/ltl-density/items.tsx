import React, { useMemo } from "react"

import { NumberInput } from "@components/input"

import { FreightClass, freightClassReference } from "./freight-class-reference"

export interface Item {
    id: string
    name: string
    inchLength: number
    inchWidth: number
    inchHeight: number
    poundsPerUnit: number
}

function Item(props: { item: Item; updateItem: (item: Item) => void; deleteItem: () => void }) {
    /**************************************************************************/
    /* State */
    const density: number | undefined = useMemo(() => {
        if (!props.item.poundsPerUnit) {
            return
        }

        if (!props.item.inchLength) {
            return
        }

        if (!props.item.inchWidth) {
            return
        }

        if (!props.item.inchHeight) {
            return
        }

        return (
            props.item.poundsPerUnit /
            ((props.item.inchLength / 12) * (props.item.inchWidth / 12) * (props.item.inchHeight / 12))
        )
    }, [props.item])

    const estimatedClass: FreightClass["freightClass"] | undefined = useMemo(() => {
        if (!density) {
            return
        }

        return freightClassReference.find((freightClass) => {
            if (freightClass.max) {
                return density < freightClass.max
            } else if (freightClass.min) {
                return density >= freightClass.min
            }
        })?.freightClass
    }, [density])

    /**************************************************************************/
    /* Render */
    return (
        <div className="border-b-[1px] border-slate-300 pb-4">
            <div className="flex justify-between">
                <h3 className="text-xl font-semibold">{props.item.name}</h3>

                <button
                    className="btn btn-sm btn-primary-text"
                    onClick={props.deleteItem}
                >
                    Remove
                </button>
            </div>

            <div className="mt-4 flex flex-wrap gap-4">
                <NumberInput
                    className="w-full flex-shrink-0 md:w-[120px]"
                    label="Length (in)"
                    step={0.01}
                    value={props.item.inchLength}
                    setValue={(value) => {
                        props.updateItem({
                            ...props.item,
                            inchLength: value,
                        })
                    }}
                />

                <NumberInput
                    className="w-full flex-shrink-0 md:w-[120px]"
                    label="Width (in)"
                    step={0.01}
                    value={props.item.inchWidth}
                    setValue={(value) => {
                        props.updateItem({
                            ...props.item,
                            inchWidth: value,
                        })
                    }}
                />

                <NumberInput
                    className="w-full flex-shrink-0 md:w-[120px]"
                    label="Height (in)"
                    step={0.01}
                    value={props.item.inchHeight}
                    setValue={(value) => {
                        props.updateItem({
                            ...props.item,
                            inchHeight: value,
                        })
                    }}
                />

                <NumberInput
                    className="w-full flex-shrink-0 md:w-[180px]"
                    label="Weight per Unit (lbs)"
                    step={0.01}
                    value={props.item.poundsPerUnit}
                    setValue={(value) => {
                        props.updateItem({
                            ...props.item,
                            poundsPerUnit: value,
                        })
                    }}
                />
            </div>

            {density && (
                <h4 className="mt-2 text-xl font-semibold">
                    Density: {density.toFixed(2)} lb{density === 1 ? "" : "s"} / ft<sup>3</sup>
                </h4>
            )}

            {estimatedClass && <h4 className="mt-2 text-xl font-semibold">Estimated Class: {estimatedClass}</h4>}
        </div>
    )
}

export function ItemList(props: {
    items: Array<Item>
    updateItems: React.Dispatch<React.SetStateAction<Array<Item>>>
}) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="mt-4 flex flex-col gap-4">
            {props.items.map((item) => {
                return (
                    <Item
                        key={item.id}
                        item={item}
                        updateItem={(updatedItem) => {
                            props.updateItems((prevState) => {
                                return prevState.map((prevItem) => {
                                    if (prevItem.id !== item.id) {
                                        return prevItem
                                    }

                                    return updatedItem
                                })
                            })
                        }}
                        deleteItem={() => {
                            props.updateItems((prevState) => {
                                return prevState.filter((prevItem) => {
                                    return prevItem.id !== item.id
                                })
                            })
                        }}
                    />
                )
            })}
        </div>
    )
}

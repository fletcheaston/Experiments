"use client"

import {useLiveQuery} from "dexie-react-hooks"
import React, {useEffect, useState} from "react"

import {Equipment, database} from "@components/database"
import {Divider} from "@components/divider"
import {NumberInput, TextInput} from "@components/input"
import Modal from "@components/modal"
import {Table} from "@components/table"
import {Loading} from "@components/loading"


function AddEquipment() {
    /**************************************************************************/
    /* State */
    const [open, setOpen] = useState(false)
    const [saving, setSaving] = useState(false)

    const [name, setName] = useState("")
    const [inchLength, setInchLength] = useState(100.0)
    const [inchWidth, setInchWidth] = useState(100.0)
    const [inchHeight, setInchHeight] = useState(100.0)
    const [poundsMaxWeight, setPoundsMaxWeight] = useState(10000.0)

    /**************************************************************************/
    /* Render */
    return (
        <>
            <button
                className="btn btn-primary"
                onClick={() => setOpen(true)}
            >
                Add Equipment
            </button>

            <Modal
                open={open}
                close={() => setOpen(false)}
                title="Add Equipment"
            >
                <>
                    <Divider className="mt-4"/>

                    <form
                        className="mt-6 flex flex-col gap-6"
                        onSubmit={async (event) => {
                            setSaving(true)
                            event.preventDefault()

                            // Add the equipment
                            await database.equipment.add({
                                id: crypto.randomUUID(),
                                created: new Date(),
                                name,
                                inchLength,
                                inchWidth,
                                inchHeight,
                                poundsMaxWeight,
                            })

                            // Reset state
                            setOpen(false)
                            setSaving(false)
                            setName("")
                            setInchLength(100.0)
                            setInchWidth(100.0)
                            setInchHeight(100.0)
                            setPoundsMaxWeight(10000.0)
                        }}
                    >
                        <div className="flex gap-x-4">
                            <TextInput
                                label="Equipment Name"
                                placeholder="Truck"
                                value={name}
                                required
                                setValue={setName}
                            />

                            <NumberInput
                                label="Max Weight (lbs)"
                                step={0.01}
                                min={0.01}
                                required
                                value={poundsMaxWeight}
                                setValue={setPoundsMaxWeight}
                            />
                        </div>

                        <div className="flex gap-x-4">
                            <NumberInput
                                label="Length (in)"
                                step={0.01}
                                min={0.01}
                                required
                                value={inchLength}
                                setValue={setInchLength}
                            />

                            <NumberInput
                                label="Width (in)"
                                step={0.01}
                                min={0.01}
                                required
                                value={inchWidth}
                                setValue={setInchWidth}
                            />

                            <NumberInput
                                label="Height (in)"
                                step={0.01}
                                min={0.01}
                                required
                                value={inchHeight}
                                setValue={setInchHeight}
                            />
                        </div>

                        <Divider/>

                        <div>
                            <button
                                className="btn btn-primary"
                                type="submit"
                                disabled={saving}
                            >
                                Save
                            </button>
                        </div>
                    </form>
                </>
            </Modal>
        </>
    )
}

function EditEquipment(props: { equipment: Equipment; close: () => void }) {
    /**************************************************************************/
    /* State */
    const [saving, setSaving] = useState(false)

    const [name, setName] = useState(props.equipment.name)
    const [inchLength, setInchLength] = useState(props.equipment.inchLength)
    const [inchWidth, setInchWidth] = useState(props.equipment.inchWidth)
    const [inchHeight, setInchHeight] = useState(props.equipment.inchHeight)
    const [poundsMaxWeight, setPoundsMaxWeight] = useState(props.equipment.poundsMaxWeight)

    /**************************************************************************/
    /* Render */
    return (
        <Modal
            open={true}
            close={props.close}
            title="Edit Equipment"
        >
            <>
                <Divider className="mt-4"/>

                <form
                    className="mt-6 flex flex-col gap-6"
                    onSubmit={async (event) => {
                        setSaving(true)
                        event.preventDefault()

                        // Modify the equipment
                        await database.equipment.where({id: props.equipment.id}).modify({
                            name,
                            inchLength,
                            inchWidth,
                            inchHeight,
                            poundsMaxWeight,
                        })

                        // Close the editor
                        props.close()
                    }}
                >
                    <div className="flex gap-x-4">
                        <TextInput
                            label="Equipment Name"
                            placeholder="Truck"
                            value={name}
                            required
                            setValue={setName}
                        />

                        <NumberInput
                            label="Max Weight (lbs)"
                            step={0.01}
                            min={0.01}
                            required
                            value={poundsMaxWeight}
                            setValue={setPoundsMaxWeight}
                        />
                    </div>

                    <div className="flex gap-x-4">
                        <NumberInput
                            label="Length (in)"
                            step={0.01}
                            min={0.01}
                            required
                            value={inchLength}
                            setValue={setInchLength}
                        />

                        <NumberInput
                            label="Width (in)"
                            step={0.01}
                            min={0.01}
                            required
                            value={inchWidth}
                            setValue={setInchWidth}
                        />

                        <NumberInput
                            label="Height (in)"
                            step={0.01}
                            min={0.01}
                            required
                            value={inchHeight}
                            setValue={setInchHeight}
                        />
                    </div>

                    <Divider/>

                    <div className="flex justify-between">
                        <button
                            className="btn btn-primary"
                            type="submit"
                            disabled={saving}
                        >
                            Save
                        </button>

                        <button
                            className="btn btn-primary-text"
                            type="button"
                            onClick={async () => {
                                await database.equipment.delete(props.equipment.id)
                            }}
                            disabled={saving}
                        >
                            Delete Equipment
                        </button>
                    </div>
                </form>
            </>
        </Modal>
    )
}

export function Equipment() {
    /**************************************************************************/
    /* State */
    const rawEquipment = useLiveQuery(() => database.equipment.orderBy("created").toArray())
    const [equipment, setEquipment] = useState(rawEquipment)
    const [equipmentToEdit, setEquipmentToEdit] = useState<Equipment | null>(null)

    const loading = rawEquipment === undefined
    const hasEquipment = equipment !== undefined && equipment.length > 0

    /**************************************************************************/
    /* Effects */
    // Only refresh the equipment list when it's loaded
    useEffect(() => {
        if (!rawEquipment) {
            return
        }

        setEquipment(rawEquipment)
    }, [rawEquipment])

    // If the equipment being edited is deleted, reset the equipment to edit
    useEffect(() => {
        if (!equipmentToEdit || !equipment) {
            return
        }

        if (
            !equipment.find((row) => {
                return row.id === equipmentToEdit.id
            })
        ) {
            setEquipmentToEdit(null)
        }
    }, [equipment, equipmentToEdit])

    /**************************************************************************/
    /* Render */
    return (
        <div>
            <div className="rounded border-[1px] border-slate-300 p-2">
                <div className="flex items-end justify-between gap-x-16">
                    <h2 className="text-3xl font-semibold">My Equipment</h2>

                    <AddEquipment/>
                </div>

                <p className="mt-3 text-[0.875rem]">
                    Edit all your custom equipment.
                </p>

                {equipmentToEdit && (
                    <EditEquipment
                        equipment={equipmentToEdit}
                        close={() => {
                            setEquipmentToEdit(null)
                        }}
                    />
                )}

                {hasEquipment && (
                    <div className="mt-2">
                        <Loading on={loading}>
                            <Table
                                columns={[
                                    {
                                        title: "Name",
                                        width: "158px",
                                        align: "left",
                                        renderer: (row) => {
                                            return row.name
                                        },
                                    },
                                    {
                                        title: "Inner Dims (in)",
                                        width: "150px",
                                        align: "right",
                                        renderer: (row) => {
                                            return `${row.inchLength}x${row.inchWidth}x${row.inchHeight}`
                                        },
                                    },
                                    {
                                        title: "",
                                        width: "70px",
                                        align: "center",
                                        renderer: (row) => {
                                            return (
                                                <button
                                                    className="btn btn-sm btn-primary-text"
                                                    onClick={() => {
                                                        setEquipmentToEdit(row)
                                                    }}
                                                >
                                                    Edit
                                                </button>
                                            )
                                        },
                                    },
                                ]}
                                rows={equipment}
                            />
                        </Loading>
                    </div>
                )}
            </div>
        </div>
    )
}

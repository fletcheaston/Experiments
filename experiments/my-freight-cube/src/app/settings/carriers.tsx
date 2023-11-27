"use client"

import { useLiveQuery } from "dexie-react-hooks"
import React, { useEffect, useState } from "react"

import { Carrier, database } from "@components/database"
import { Divider } from "@components/divider"
import { NumberInput, TextInput } from "@components/input"
import { Loading } from "@components/loading"
import Modal from "@components/modal"
import { Table } from "@components/table"

function AddCarrier() {
    /**************************************************************************/
    /* State */
    const [open, setOpen] = useState(false)
    const [saving, setSaving] = useState(false)

    const [name, setName] = useState("")
    const [dimDivisor, setDimDivisor] = useState(0.01)

    /**************************************************************************/
    /* Render */
    return (
        <>
            <button
                className="btn btn-primary"
                onClick={() => setOpen(true)}
            >
                Add Carrier
            </button>

            <Modal
                open={open}
                close={() => setOpen(false)}
                title="Add Carrier"
            >
                <>
                    <Divider className="mt-4" />

                    <form
                        className="mt-6 flex flex-col gap-6"
                        onSubmit={async (event) => {
                            setSaving(true)
                            event.preventDefault()

                            // Add the carrier
                            await database.carriers.add({
                                id: crypto.randomUUID(),
                                created: new Date(),
                                name,
                                dimDivisor,
                            })

                            // Reset state
                            setOpen(false)
                            setSaving(false)
                            setName("")
                            setDimDivisor(0.01)
                        }}
                    >
                        <div className="flex gap-x-4">
                            <TextInput
                                label="Carrier Name"
                                placeholder="MyFreightCube"
                                value={name}
                                required
                                setValue={setName}
                            />

                            <NumberInput
                                label="Dim Divisor"
                                step={0.01}
                                min={0.01}
                                required
                                value={dimDivisor}
                                setValue={setDimDivisor}
                            />
                        </div>

                        <Divider />

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

function EditCarrier(props: { carrier: Carrier; close: () => void }) {
    /**************************************************************************/
    /* State */
    const [saving, setSaving] = useState(false)

    const [name, setName] = useState(props.carrier.name)
    const [dimDivisor, setDimDivisor] = useState(props.carrier.dimDivisor)

    /**************************************************************************/
    /* Render */
    return (
        <Modal
            open={true}
            close={props.close}
            title="Edit Carrier"
        >
            <>
                <Divider className="mt-4" />

                <form
                    className="mt-6 flex flex-col gap-6"
                    onSubmit={async (event) => {
                        setSaving(true)
                        event.preventDefault()

                        // Modify the carrier
                        await database.carriers.where({ id: props.carrier.id }).modify({
                            name,
                            dimDivisor,
                        })

                        // Close the editor
                        props.close()
                    }}
                >
                    <div className="flex gap-x-4">
                        <TextInput
                            label="Carrier Name"
                            placeholder="MyFreightCube"
                            value={name}
                            required
                            setValue={setName}
                        />

                        <NumberInput
                            label="Dim Divisor"
                            step={0.01}
                            min={0.01}
                            required
                            value={dimDivisor}
                            setValue={setDimDivisor}
                        />
                    </div>

                    <Divider />

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
                                await database.carriers.delete(props.carrier.id)
                            }}
                            disabled={saving}
                        >
                            Delete Carrier
                        </button>
                    </div>
                </form>
            </>
        </Modal>
    )
}

export function Carriers() {
    /**************************************************************************/
    /* State */
    const rawCarriers = useLiveQuery(() => database.carriers.orderBy("created").toArray())
    const [carriers, setCarriers] = useState(rawCarriers)
    const [carrierToEdit, setCarrierToEdit] = useState<Carrier | null>(null)

    const loading = rawCarriers === undefined
    const hasCarriers = carriers !== undefined && carriers.length > 0

    /**************************************************************************/
    /* Effects */
    // Only refresh the carrier list when it's loaded
    useEffect(() => {
        if (!rawCarriers) {
            return
        }

        setCarriers(rawCarriers)
    }, [rawCarriers])

    // If the carrier being edited is deleted, reset the carrier to edit
    useEffect(() => {
        if (!carrierToEdit || !carriers) {
            return
        }

        if (
            !carriers.find((row) => {
                return row.id === carrierToEdit.id
            })
        ) {
            setCarrierToEdit(null)
        }
    }, [carriers, carrierToEdit])

    /**************************************************************************/
    /* Render */
    return (
        <div>
            <div className="rounded border-[1px] border-slate-300 p-2">
                <div className="flex items-end justify-between gap-x-16">
                    <h2 className="text-3xl font-semibold">My Carriers</h2>

                    <AddCarrier />
                </div>

                <p className="mt-3 text-[0.875rem]">Edit all your custom carriers.</p>

                {carrierToEdit && (
                    <EditCarrier
                        carrier={carrierToEdit}
                        close={() => {
                            setCarrierToEdit(null)
                        }}
                    />
                )}

                {hasCarriers && (
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
                                        title: "Dim Divisor",
                                        width: "130px",
                                        align: "right",
                                        renderer: (row) => {
                                            return row.dimDivisor
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
                                                        setCarrierToEdit(row)
                                                    }}
                                                >
                                                    Edit
                                                </button>
                                            )
                                        },
                                    },
                                ]}
                                rows={carriers}
                            />
                        </Loading>
                    </div>
                )}
            </div>
        </div>
    )
}

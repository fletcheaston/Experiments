"use client"

import { useLiveQuery } from "dexie-react-hooks"
import React, { useEffect, useState } from "react"

import { Carrier, database } from "@components/database"
import { Divider } from "@components/divider"
import { CheckboxInput, NumberInput, TextInput } from "@components/input"
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
    const [defaultCarrier, setDefaultCarrier] = useState(false)

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
                        className="mt-4 flex flex-col gap-4"
                        onSubmit={async (event) => {
                            setSaving(true)
                            event.preventDefault()

                            // If this is the new default carrier, remove the default from all other carriers
                            if (defaultCarrier) {
                                await database.carriers
                                    .where({ default: "default" })
                                    .modify((carrier) => (carrier.default = null))
                            }

                            // Add the carrier
                            await database.carriers.add({
                                id: crypto.randomUUID(),
                                created: new Date(),
                                default: defaultCarrier ? "default" : null,
                                name,
                                dimDivisor,
                            })

                            // Reset state
                            setOpen(false)
                            setSaving(false)
                            setName("")
                            setDimDivisor(0.01)
                            setDefaultCarrier(false)
                        }}
                    >
                        <TextInput
                            label="Carrier Name"
                            placeholder="MyFreightCube"
                            value={name}
                            required
                            setValue={setName}
                        />

                        <div className="flex gap-x-6">
                            <div className="w-[40%]">
                                <NumberInput
                                    label="Dim Divisor"
                                    placeholder={0.01}
                                    step={0.01}
                                    min={0.01}
                                    required
                                    value={dimDivisor}
                                    setValue={setDimDivisor}
                                />
                            </div>

                            <div className="mt-3.5">
                                <CheckboxInput
                                    label="Default Carrier"
                                    checked={defaultCarrier}
                                    setChecked={setDefaultCarrier}
                                />
                            </div>
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
    const [defaultCarrier, setDefaultCarrier] = useState(props.carrier.default === "default")

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
                    className="mt-4 flex flex-col gap-4"
                    onSubmit={async (event) => {
                        setSaving(true)
                        event.preventDefault()

                        // If this is the new default carrier, remove the default from all other carriers
                        if (defaultCarrier) {
                            await database.carriers
                                .where({ default: "default" })
                                .modify((carrier) => (carrier.default = null))
                        }

                        // Modify the carrier
                        await database.carriers.where({ id: props.carrier.id }).modify({
                            default: defaultCarrier ? "default" : null,
                            name,
                            dimDivisor,
                        })

                        // Close the editor
                        props.close()
                    }}
                >
                    <TextInput
                        label="Carrier Name"
                        placeholder="MyFreightCube"
                        value={name}
                        required
                        setValue={setName}
                    />

                    <div className="flex gap-x-6">
                        <div className="w-[40%]">
                            <NumberInput
                                label="Dim Divisor"
                                placeholder={0.01}
                                step={0.01}
                                min={0.01}
                                required
                                value={dimDivisor}
                                setValue={setDimDivisor}
                            />
                        </div>

                        <div className="mt-3.5">
                            <CheckboxInput
                                label="Default Carrier"
                                checked={defaultCarrier}
                                setChecked={setDefaultCarrier}
                            />
                        </div>
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
    const loading = rawCarriers === undefined

    const [carrierToEdit, setCarrierToEdit] = useState<Carrier | null>(null)

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
            !carriers.find((carrier) => {
                return carrier.id === carrierToEdit.id
            })
        ) {
            setCarrierToEdit(null)
        }
    }, [carriers, carrierToEdit])

    /**************************************************************************/
    /* Render */
    return (
        <div>
            <div className="flex items-end justify-between gap-x-16">
                <h2 className="mt-6 text-3xl font-semibold">My Carriers</h2>

                <AddCarrier />
            </div>

            {carrierToEdit && (
                <EditCarrier
                    carrier={carrierToEdit}
                    close={() => {
                        setCarrierToEdit(null)
                    }}
                />
            )}

            <div className="mt-4">
                <Loading on={loading}>
                    <Table
                        columns={[
                            {
                                title: "Name",
                                width: "200px",
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
                                title: "Default",
                                width: "75px",
                                align: "center",
                                renderer: (row) => {
                                    return row.default === "default" ? (
                                        <div className="font-bold text-rose-700">✓</div>
                                    ) : (
                                        ""
                                    )
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
        </div>
    )
}

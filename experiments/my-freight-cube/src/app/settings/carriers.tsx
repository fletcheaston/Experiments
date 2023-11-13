"use client"

import { useLiveQuery } from "dexie-react-hooks"
import { useState } from "react"

import { database } from "@components/database"
import { Divider } from "@components/divider"
import { NumberInput, TextInput } from "@components/input"
import { Loading } from "@components/loading"
import Modal from "@components/modal"

export function AddCarrier() {
    /**************************************************************************/
    /* State */
    const [open, setOpen] = useState(false)

    const [name, setName] = useState("")
    const [dimDivisor, setDimDivisor] = useState(0.01)
    const [defaultCarrier] = useState(false)

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
                        onSubmit={async () => {
                            await database.carriers.add({
                                id: crypto.randomUUID(),
                                created: new Date(),
                                default: defaultCarrier,
                                name,
                                dimDivisor,
                            })

                            setOpen(false)
                        }}
                    >
                        <TextInput
                            label="Carrier Name"
                            placeholder="MyFreightCube"
                            value={name}
                            required
                            setValue={setName}
                        />

                        <NumberInput
                            label="Dim Divisor"
                            placeholder={0.01}
                            step={0.01}
                            min={0.01}
                            required
                            value={dimDivisor}
                            setValue={setDimDivisor}
                        />

                        <Divider />

                        <div className="flex justify-between">
                            <button
                                className="btn btn-primary"
                                type="submit"
                            >
                                Save
                            </button>

                            <button
                                className="btn btn-primary-text"
                                type="reset"
                                onClick={() => setOpen(false)}
                            >
                                Discard
                            </button>
                        </div>
                    </form>
                </>
            </Modal>
        </>
    )
}

export function CarriersList() {
    /**************************************************************************/
    /* State */
    const carriers = useLiveQuery(() => database.carriers.orderBy("created").toArray())

    /**************************************************************************/
    /* Render */
    if (carriers === undefined) {
        return <Loading />
    }

    return (
        <>
            {carriers.map((carrier) => {
                return <div key={carrier.id}>{carrier.name}</div>
            })}
        </>
    )
}

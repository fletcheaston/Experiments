"use client"

import Dexie, { Table } from "dexie"

interface Base {
    id: string
    created: Date
    default: boolean | null
}

export interface Carrier extends Base {
    name: string
    dimDivisor: number
}

export interface Equipment extends Base {
    name: string
    inchLength: number
    inchWidth: number
    inchHeight: number
    poundsMaxWeight: number
}

export class DexieDatabase extends Dexie {
    carriers!: Table<Carrier>
    equipment!: Table<Equipment>

    constructor() {
        super("myFreightCube")
        this.version(1).stores({
            carriers: "id,created,&default",
            equipment: "id,created,&default",
        })
    }
}

export const database = new DexieDatabase()

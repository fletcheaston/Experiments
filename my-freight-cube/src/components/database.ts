"use client"

import Dexie, { Table } from "dexie"

interface Base {
    id: string
    created: Date
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
        this.version(2).stores({
            carriers: "id,created",
            equipment: "id,created",
        })
    }
}

export const database = new DexieDatabase()

"use client"

import { Menu, Transition } from "@headlessui/react"
import classNames from "classnames"
import Link from "next/link"
import React, { Fragment } from "react"

import { Divider } from "@components/divider"

interface LinkProps extends Pick<React.ComponentProps<typeof Link>, "href" | "children"> {
    type: "link"
}

interface Divide {
    type: "divider"
    id: string
}

type Item = LinkProps | Divide

export function Dropdown({ title, items }: { title: React.ReactNode; items: Array<Item> }) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="text-right">
            <Menu
                as="div"
                className="relative inline-block text-left"
            >
                {({ open }) => (
                    <>
                        <Menu.Button
                            className={classNames(
                                "btn btn-lg inline-flex w-full justify-center",
                                open ? "btn-primary" : "btn-primary-text",
                            )}
                        >
                            {title}
                        </Menu.Button>

                        <Transition
                            as={Fragment}
                            show={open}
                            enter="transition ease-out duration-100"
                            enterFrom="transform opacity-0 scale-95"
                            enterTo="transform opacity-100 scale-100"
                            leave="transition ease-in duration-75"
                            leaveFrom="transform opacity-100 scale-100"
                            leaveTo="transform opacity-0 scale-95"
                        >
                            <Menu.Items className="absolute right-0 mt-2 w-fit origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-black/5 focus:outline-none">
                                {items.map((item) => {
                                    if (item.type === "divider") {
                                        return <Divider key={item.id} />
                                    }

                                    return (
                                        <Menu.Item key={item.href.toString()}>
                                            <div className="btn whitespace-nowrap px-0 text-left">
                                                <Link
                                                    href={item.href}
                                                    className=""
                                                >
                                                    <div className="w-full px-6">{item.children}</div>
                                                </Link>
                                            </div>
                                        </Menu.Item>
                                    )
                                })}
                            </Menu.Items>
                        </Transition>
                    </>
                )}
            </Menu>
        </div>
    )
}
